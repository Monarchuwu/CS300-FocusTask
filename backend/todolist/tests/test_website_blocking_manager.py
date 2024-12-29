import pytest
from unittest.mock import patch, MagicMock
from todolist.models.managers import WebsiteBlockingManager, UserManager
from django.db.utils import IntegrityError

@pytest.fixture
def mock_database():
    with patch("todolist.models.databases.WebsiteBlockingDB") as MockDB, \
         patch("todolist.models.databases.UserDB") as MockUserDB:
        yield MockDB, MockUserDB

def test_get_block_list(mock_database):
    mock_website_db, _ = mock_database

    mock_records = [
        MagicMock(get_data_object=lambda: {"URL": "example.com"}),
        MagicMock(get_data_object=lambda: {"URL": "test.com"}),
    ]
    mock_website_db.objects.filter.return_value = mock_records

    manager = WebsiteBlockingManager()
    result = manager.getBlockList(1)

    assert result == [
        {"URL": "example.com"},
        {"URL": "test.com"},
    ]

@pytest.mark.django_db
def test_add_to_block_list(mock_database):
    mock_website_db, mock_user_db = mock_database

    # Mock the user returned by UserDB.objects.get
    mock_user_instance = MagicMock()
    mock_user_db.objects.get.return_value = mock_user_instance

    # Mock the WebsiteBlockingDB instance and its save method
    mock_block_instance = MagicMock()
    mock_website_db.return_value = mock_block_instance

    manager = WebsiteBlockingManager()
    result = manager.addToBlockList(1, "example.com")

    mock_user_db.objects.get.assert_called_once_with(userID=1)
    mock_block_instance.save.assert_called_once()
    assert result == "Website 'example.com' added to block list."

@pytest.mark.django_db
def test_add_to_block_list_duplicate(mock_database):
    mock_website_db, _ = mock_database
    mock_website_db.side_effect = IntegrityError

    manager = WebsiteBlockingManager()
    with pytest.raises(ValueError, match="Website example.com already in block list"):
        manager.addToBlockList(1, "example.com")

@pytest.mark.django_db
def test_delete_from_block_list(mock_database):
    mock_website_db, mock_user_db = mock_database

    # Mock UserDB to return the user instance
    mock_user_instance = MagicMock()
    mock_user_db.objects.get.return_value = mock_user_instance

    # Mock filter return value and its delete method
    mock_filter = MagicMock()
    mock_website_db.objects.filter.return_value = mock_filter

    manager = WebsiteBlockingManager()
    result = manager.deleteFromBlockList(1, 123)

    mock_website_db.objects.filter.assert_called_once_with(blockID=123, UserID=mock_user_instance)
    mock_filter.delete.assert_called_once()
    assert result == "BlockID 123 removed from block list."

@pytest.mark.django_db
def test_toggle_block(mock_database):
    mock_website_db, _ = mock_database

    # Mock get return value
    mock_entry = MagicMock(isBlocking=True)
    mock_website_db.objects.get.return_value = mock_entry

    manager = WebsiteBlockingManager()
    result = manager.toggleBlock(1, 123)

    # Assert toggling behavior
    assert result == "BlockID 123 toggled to not blocking."
    assert mock_entry.isBlocking is False
    mock_entry.save.assert_called_once()

@pytest.mark.django_db
def test_set_block(mock_database):
    mock_website_db, _ = mock_database

    # Mock get return value
    mock_entry = MagicMock()
    mock_website_db.objects.get.return_value = mock_entry

    manager = WebsiteBlockingManager()
    result = manager.setBlock(1, 123, True)

    # Assert setting behavior
    assert result == "BlockID 123 set to blocking."
    assert mock_entry.isBlocking is True
    mock_entry.save.assert_called_once()