import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from todolist.models.managers import PomodoroManager
from todolist.models.objects import PomodoroHistory, TodoItem
from todolist.models import databases

@pytest.fixture
def pomodoro_manager():
    return PomodoroManager()

@pytest.fixture
def sample_task():
    """Fixture for a sample TodoItem object."""
    return TodoItem(
        itemID=1,
        name="Sample Task",
        parentID=None,
        createdDate=datetime.now(),
        userID=1,
        itemType="Task",
        labelID=None,
    )


@pytest.fixture
def sample_pomodoroHistory():
    """Fixture for a sample Preference object."""
    return PomodoroHistory(
        pomodoroID = 1,
        taskID = 1,
        startTime = datetime.now(),
        duration = timedelta(minutes = 30),
        endTime = None,
        status = databases.PomodoroHistoryDB.Status.CANCELED,
        createdAt = datetime.now()
    )

@pytest.mark.django_db
def test_set_task_id(pomodoro_manager, sample_pomodoroHistory):
    """Test successful modification of taskID."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.create") as mock_create_pomo, \
            patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get_task:
        mock_get_task.return_value = MagicMock(taskID = sample_pomodoroHistory.taskID)
        mock_create_pomo.return_value = MagicMock()

        pomodoro_manager.setTaskID(sample_pomodoroHistory.taskID)

        mock_get_task.assert_called_once_with(taskID = sample_pomodoroHistory.taskID)
        mock_create_pomo.assert_called_once()
        assert mock_create_pomo.call_args[1]["taskID"] == sample_pomodoroHistory.taskID

def test_set_task_id_not_found(pomodoro_manager, sample_pomodoroHistory):
    """Test successful modification of taskID."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.create") as mock_create_pomo, \
            patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get_task:
        mock_get_task.return_value = MagicMock(taskID = sample_pomodoroHistory.taskID - 12)
        mock_get_task.side_effect = databases.TodoItemDB.DoesNotExist
        mock_create_pomo.return_value = MagicMock()
        with pytest.raises(ValueError) as excinfo:
            pomodoro_manager.setTaskID(sample_pomodoroHistory.taskID - 12)
        assert str(excinfo.value) == f"Task ID {sample_pomodoroHistory.taskID - 12} do not exist."
        mock_get_task.assert_called_once_with(taskID = sample_pomodoroHistory.taskID - 12)
        mock_create_pomo.assert_not_called()

def test_set_time(pomodoro_manager, sample_pomodoroHistory):
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomo:
        mock_pomo_instance = MagicMock()
        mock_get_pomo.return_value = mock_pomo_instance

        pomodoro_manager.setTime(sample_pomodoroHistory.pomodoroID, sample_pomodoroHistory.duration)

        mock_get_pomo.assert_called_once_with(pomodoroID = sample_pomodoroHistory.pomodoroID)
        assert mock_pomo_instance.duration == sample_pomodoroHistory.duration
        assert mock_pomo_instance.currentDuration == sample_pomodoroHistory.duration
        mock_pomo_instance.save.assert_called_once()

def test_start_pomodoro_success(pomodoro_manager):
    """Test starting a pomodoro successfully."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomodoro:
        # Mock the pomodoro instance
        mock_pomodoro = MagicMock()
        mock_pomodoro.status = "Canceled"  # Simulate the status
        mock_get_pomodoro.return_value = mock_pomodoro

        # Call the method
        pomodoro_manager.start(1)

        # Assert the mocked interactions
        mock_get_pomodoro.assert_called_once_with(pomodoroID=1)
        assert mock_pomodoro.status == "Running"
        mock_pomodoro.save.assert_called_once()


def test_unpause_pomodoro_success(pomodoro_manager):
    """Test unpausing a pomodoro successfully."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomodoro:
        # Mock the pomodoro instance
        mock_pomodoro = MagicMock()
        mock_pomodoro.status = "Paused"  # Simulate the status
        mock_get_pomodoro.return_value = mock_pomodoro

        # Call the method
        pomodoro_manager.unpause(1)

        # Assert the mocked interactions
        mock_get_pomodoro.assert_called_once_with(pomodoroID=1)
        assert mock_pomodoro.status == "Running"
        mock_pomodoro.save.assert_called_once()


def test_pause_pomodoro_success(pomodoro_manager):
    """Test pausing a pomodoro successfully."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomodoro:
        # Mock the pomodoro instance
        mock_pomodoro = MagicMock()
        mock_pomodoro.status = "Running"  # Simulate the status
        mock_pomodoro.endTime = datetime.now() - timedelta(minutes=5)
        mock_pomodoro.currentDuration = timedelta(minutes=25)
        mock_get_pomodoro.return_value = mock_pomodoro

        # Call the method
        pomodoro_manager.pause(1)

        # Assert the mocked interactions
        mock_get_pomodoro.assert_called_once_with(pomodoroID=1)
        assert mock_pomodoro.status == "Paused"
        assert mock_pomodoro.currentDuration > timedelta(0)
        mock_pomodoro.save.assert_called_once()


def test_get_time_success(pomodoro_manager):
    """Test getting the remaining time of a pomodoro."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomodoro, \
         patch.object(pomodoro_manager, "end") as mock_end:
        # Mock the pomodoro instance
        mock_pomodoro = MagicMock()
        mock_pomodoro.endTime = datetime.now() - timedelta(minutes=5)
        mock_pomodoro.currentDuration = timedelta(minutes=25)
        mock_get_pomodoro.return_value = mock_pomodoro

        # Call the method
        remaining_time = pomodoro_manager.getTime(1)

        # Assert the mocked interactions
        mock_get_pomodoro.assert_called_once_with(pomodoroID=1)
        assert remaining_time.total_seconds() > 0
        mock_pomodoro.save.assert_called_once()


def test_end_pomodoro_success(pomodoro_manager):
    """Test ending a pomodoro successfully."""
    with patch("todolist.models.managers.databases.PomodoroHistoryDB.objects.get") as mock_get_pomodoro:
        # Mock the pomodoro instance
        mock_pomodoro = MagicMock()
        mock_get_pomodoro.return_value = mock_pomodoro

        # Call the method
        pomodoro_manager.end(1)

        # Assert the mocked interactions
        mock_get_pomodoro.assert_called_once_with(pomodoroID=1)
        assert mock_pomodoro.status == "Completed"
        mock_pomodoro.save.assert_called_once()