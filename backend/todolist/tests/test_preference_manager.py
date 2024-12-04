import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from todolist.models.managers import PreferencesManager
from todolist.models.objects import Preferences, User
from todolist.models import databases

@pytest.fixture
def preferences_manager():
    return PreferencesManager()

@pytest.fixture
def sample_user():
    """Fixture for a sample User object."""
    return User(
        userID=1,
        username="Sample User",
        email="@gmail.com",
        passwordHash = "1234",
        avatarURL = None,
        createdAt = datetime.now()
    )

@pytest.fixture
def sample_preference():
    """Fixture for a sample Preference object."""
    return Preferences(
        userID = 1,
        language = "English",
        timezone = "UTC+0",
        notification = False,
        autoBlock = True
    )

@pytest.mark.django_db
def test_set_language_user(preferences_manager, sample_preference):
    """Test successful modification of a language."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        preferences_manager.setLanguage(userID=sample_preference.userID, language = databases.PreferencesDB.Language.VIETNAMESE)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert mock_pref_instance.language == databases.PreferencesDB.Language.VIETNAMESE
        mock_pref_instance.save.assert_called_once()

@pytest.mark.django_db
def test_set_timezone_user(preferences_manager, sample_preference):
    """Test successful modification of a timezone."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        preferences_manager.setTimezone(userID=sample_preference.userID, timezone = databases.PreferencesDB.Timezone.UTC2)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert mock_pref_instance.timezone == databases.PreferencesDB.Timezone.UTC2
        mock_pref_instance.save.assert_called_once()

@pytest.mark.django_db
def test_set_notification_user(preferences_manager, sample_preference):
    """Test successful modification of notification."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        preferences_manager.setNotification(userID=sample_preference.userID, status=True)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert mock_pref_instance.notification == True
        mock_pref_instance.save.assert_called_once()

@pytest.mark.django_db
def test_set_autoblock_user(preferences_manager, sample_preference):
    """Test successful modification of autoblock."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        preferences_manager.setAutoBlock(userID=sample_preference.userID, status = True)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert mock_pref_instance.autoBlock == True
        mock_pref_instance.save.assert_called_once()

@pytest.mark.django_db
def test_get_language_user(preferences_manager, sample_preference):
    """Test successful retrieval of a language."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_pref_instance.language = sample_preference.language  
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        language = preferences_manager.getLanguage(userID=sample_preference.userID)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert language == sample_preference.language

@pytest.mark.django_db
def test_get_timezone_user(preferences_manager, sample_preference):
    """Test successful retrieval of timezone."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_pref_instance.timezone = sample_preference.timezone 
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        timezone = preferences_manager.getTimezone(userID=sample_preference.userID)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert timezone == sample_preference.timezone

@pytest.mark.django_db
def test_get_notification_user(preferences_manager, sample_preference):
    """Test successful retrieval of notification."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_pref_instance.notification = sample_preference.notification
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        noti = preferences_manager.getNotification(userID=sample_preference.userID)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert noti == sample_preference.notification

@pytest.mark.django_db
def test_get_autoblock_user(preferences_manager, sample_preference):
    """Test successful retrieval autoblock."""
    with patch("todolist.models.managers.databases.PreferencesDB.objects.get") as mock_get_pref:
        mock_pref_instance = MagicMock()
        # Mock successful pref retrievel
        mock_pref_instance.autoBlock = sample_preference.autoBlock
        mock_get_pref.return_value = mock_pref_instance

        # Execute the method
        autoBlock = preferences_manager.getAutoBlock(userID=sample_preference.userID)

        # Assert the mocked calls
        mock_get_pref.assert_called_once_with(userID=sample_preference.userID)
        assert autoBlock == sample_preference.autoBlock