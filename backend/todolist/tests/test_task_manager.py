import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.db.models.base import ModelState
from todolist.models.managers import TaskManager
from todolist.models.objects import TodoItem, TaskAttributes
from todolist.models import databases


@pytest.fixture
def task_manager():
    """Fixture for the TaskManager instance."""
    return TaskManager()


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
def sample_task_attributes():
    """Fixture for a sample TaskAttributes object."""
    return TaskAttributes(
        taskID=1,
        dueDate=datetime.now() + timedelta(days=1),
        priority="High",
        status="Pending",
        description="Sample Task Description",
        inTodayDate=datetime(2100, 1, 1),
    )


@pytest.mark.django_db
def test_add_todo_item_success(task_manager, sample_task):
    """Test successful addition of a task."""
    with patch("todolist.models.managers.databases.UserDB.objects.get") as mock_get_user, \
         patch("todolist.models.managers.databases.TodoItemDB.save") as mock_save:
        # Mock successful user retrieval
        mock_user = MagicMock(spec=databases.UserDB)
        mock_user.id = sample_task.userID
        mock_user._state = ModelState()
        mock_get_user.return_value = mock_user
        todo_item = databases.UserDB(username="username", email="email", passwordHash="passwordHash", avatarURL="avatarURL")
        todo_item.save()
        # Mock successful task creation
        mock_save.return_value = MagicMock()

        # Execute the method
        task_manager.addTodoItem(sample_task)

        # Assert the mocked calls
        mock_get_user.assert_called_once_with(userID=sample_task.userID)
        mock_save.assert_called_once()
        #assert mock_create.call_args[1]["name"] == "Sample Task"



@pytest.mark.django_db
def test_add_todo_item_user_not_found(task_manager, sample_task):
    """Test adding a task when the user is not found."""
    with patch("todolist.models.managers.databases.UserDB.objects.get") as mock_get_user:
        mock_get_user.side_effect = Exception("User not found")
        with pytest.raises(ValueError) as excinfo:
            task_manager.addTodoItem(sample_task)
        assert "An error occurred while adding the todo item" in str(excinfo.value)


@pytest.mark.django_db
def test_edit_todo_item_success(task_manager, sample_task, sample_task_attributes):
    """Test successful editing of a task."""
    with patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get:
        mock_get.return_value = MagicMock()
        task_manager.editTodoItem(sample_task)
        mock_get.assert_called_once_with(itemID=sample_task.itemID)
    

#@pytest.mark.django_db
#def test_edit_todo_item_success(task_manager, sample_task, sample_task_attributes):
#    """Test successful editing of a task."""
#    with patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get:
#        with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get_attr:
#            mock_get.return_value = MagicMock()
#            mock_get_attr.return_value = MagicMock()
#            task_manager.editTodoItem(sample_task)
#            mock_get.assert_called_once_with(itemID=sample_task.itemID)
#            mock_get_attr.assert_called_once_with(taskID=sample_task.itemID)


@pytest.mark.django_db
def test_get_today_task_list(task_manager):
    """Test fetching today's task list."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.filter") as mock_filter:
        mock_task = MagicMock()
        mock_task.get_data_object.return_value = "Mocked Task"
        mock_filter.return_value = [mock_task]
        tasks = task_manager.getTodayTaskList(1)
        mock_filter.assert_called_once()
        assert tasks == ["Mocked Task"]


@pytest.mark.django_db
def test_toggle_task_status(task_manager):
    """Test toggling the task status."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get:
        mock_task_attr = MagicMock()
        mock_task_attr.status = "Pending"
        mock_get.return_value = mock_task_attr
        task_manager.toggleTask(1)
        assert mock_task_attr.status == "Completed"
        mock_task_attr.save.assert_called_once()

@pytest.mark.django_db
def test_get_task_list_success(task_manager):
    """Test retrieving the task list for a valid project."""
    with patch("todolist.models.managers.databases.TodoItemDB.objects.filter") as mock_filter:
        mock_task = MagicMock()
        mock_task.get_data_object.return_value = "Mocked Task"
        mock_filter.return_value = [mock_task]

        tasks = task_manager.getTaskList(1)

        mock_filter.assert_called_once_with(parentID=1)
        assert tasks == ["Mocked Task"]


@pytest.mark.django_db
def test_get_task_list_project_not_found(task_manager):
    """Test retrieving a task list for a non-existing project."""
    with patch("todolist.models.managers.databases.TodoItemDB.objects.filter") as mock_filter:
        mock_filter.side_effect = databases.TodoItemDB.DoesNotExist

        with pytest.raises(ValueError) as excinfo:
            task_manager.getTaskList(999)

        assert "999" in str(excinfo.value) and "not exist" in str(excinfo.value)


@pytest.mark.django_db
def test_delete_task_success(task_manager):
    """Test successful deletion of a task."""
    with patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get:
        mock_task = MagicMock()
        mock_task.delete.return_value = None
        mock_get.return_value = mock_task

        task_manager.deleteTodoItem(1)

        mock_get.assert_called_once_with(itemID=1)
        mock_task.delete.assert_called_once()


@pytest.mark.django_db
def test_delete_task_not_found(task_manager):
    """Test deletion of a non-existing task."""
    with patch("todolist.models.managers.databases.TodoItemDB.objects.get") as mock_get:
        mock_get.side_effect = databases.TodoItemDB.DoesNotExist

        with pytest.raises(ValueError) as excinfo:
            task_manager.deleteTodoItem(999)

        assert "999" in str(excinfo.value) and "not exist" in str(excinfo.value)


@pytest.mark.django_db
def test_add_task_to_today_success(task_manager):
    """Test adding a task to today's list successfully."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get:
        mock_task_attr = MagicMock()
        mock_get.return_value = mock_task_attr

        task_manager.addTaskToToday(1)

        mock_get.assert_called_once_with(taskID=1)
        assert mock_task_attr.inTodayDate.date() == datetime.now().date()
        mock_task_attr.save.assert_called_once()


@pytest.mark.django_db
def test_add_task_to_today_not_found(task_manager):
    """Test adding a non-existing task to today's list."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get:
        mock_get.side_effect = databases.TaskAttributesDB.DoesNotExist

        with pytest.raises(ValueError) as excinfo:
            task_manager.addTaskToToday(999)

        assert "999" in str(excinfo.value) and "not exist" in str(excinfo.value)


@pytest.mark.django_db
def test_remove_task_from_today_success(task_manager):
    """
Test removing a task from today's list successfully."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get:
        mock_task_attr = MagicMock()
        mock_get.return_value = mock_task_attr

        task_manager.removeTaskFromToday(1)

        mock_get.assert_called_once_with(taskID=1)
        assert mock_task_attr.inTodayDate == datetime(2100, 1, 1)
        mock_task_attr.save.assert_called_once()


@pytest.mark.django_db
def test_remove_task_from_today_not_found(task_manager):
    """Test removing a non-existing task from today's list."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.get") as mock_get:
        mock_get.side_effect = databases.TaskAttributesDB.DoesNotExist

        with pytest.raises(ValueError) as excinfo:
            task_manager.removeTaskFromToday(999)

        assert "999" in str(excinfo.value) and "not exist" in str(excinfo.value)


@pytest.mark.django_db
def test_suggest_today_task_success(task_manager):
    """Test suggesting tasks for today's list successfully."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.filter") as mock_filter, \
         patch("todolist.models.managers.datetime") as mock_datetime:
        # Set a fixed datetime for consistency
        fixed_now = datetime(2024, 11, 30, 3, 42, 41)
        mock_datetime.now.return_value = fixed_now

        # Mock a queryset-like behavior
        mock_task = MagicMock()
        mock_task.get_data_object.return_value = "Mocked Task"
        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = [mock_task]

        # Ensure filter returns a queryset-like object for each filter call
        mock_filter.side_effect = [mock_queryset, mock_queryset, mock_queryset, mock_queryset]

        tasks = task_manager.suggestTodayTask(1)

        # Verify the returned tasks
        assert len(tasks) == 1
        assert tasks == ["Mocked Task"]

        # Assert each filter call with matching arguments
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            dueDate__lt=fixed_now
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            dueDate__date=fixed_now.date()
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            inTodayDate__date__lt=fixed_now.date()
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING
        )



@pytest.mark.django_db
def test_suggest_today_task_no_tasks(task_manager):
    """Test suggesting tasks when no tasks are available."""
    with patch("todolist.models.managers.databases.TaskAttributesDB.objects.filter") as mock_filter, \
         patch("todolist.models.managers.datetime") as mock_datetime:
        # Set a fixed datetime for consistency
        fixed_now = datetime(2024, 11, 30, 3, 42, 41)
        mock_datetime.now.return_value = fixed_now

        # Mock a queryset-like object that returns an empty list for `order_by`
        mock_queryset = MagicMock()
        mock_queryset.order_by.return_value = []
        mock_filter.return_value = mock_queryset

        tasks = task_manager.suggestTodayTask(1)

        # Verify the returned tasks
        assert tasks == []

        # Assert filter calls
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            dueDate__lt=fixed_now
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            dueDate__date=fixed_now.date()
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING,
            inTodayDate__date__lt=fixed_now.date()
        )
        mock_filter.assert_any_call(
            taskID__userID__userID=1,
            status=databases.TaskAttributesDB.Status.PENDING
        )

