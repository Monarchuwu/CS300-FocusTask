import pytest
from unittest.mock import patch, MagicMock
from todolist.models.managers import WebsiteBlockingManager, UserManager
from django.db.utils import IntegrityError

@pytest.fixture
def mock_database():
    with patch("todolist.models.databases.WebsiteBlockingDB") as MockDB:
        yield MockDB

def test_get_block_list(mock_database):
    mock_records = [
        MagicMock(get_data_object=lambda: {"URL": "example.com"}),
        MagicMock(get_data_object=lambda: {"URL": "test.com"}),
    ]
    mock_database.objects.filter.return_value = mock_records

    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        manager = WebsiteBlockingManager()
        result = manager.getBlockList()

    assert result == [
        {"URL": "example.com"},
        {"URL": "test.com"},
    ]

def test_add_to_block_list(mock_database):
    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        mock_instance = MagicMock()
        mock_database.return_value = mock_instance

        manager = WebsiteBlockingManager()
        result = manager.addToBlockList("example.com")

    mock_instance.save.assert_called_once()
    assert result == "Website 'example.com' added to block list."

def test_add_to_block_list_duplicate(mock_database):
    mock_database.side_effect = IntegrityError
    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        manager = WebsiteBlockingManager()
        with pytest.raises(ValueError, match="Website example.com already in block list"):
            manager.addToBlockList("example.com")

def test_delete_from_block_list(mock_database):
    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        manager = WebsiteBlockingManager()
        result = manager.deleteFromBlockList(123)

    mock_database.objects.filter.assert_called_once_with(blockID=123, UserID=1)
    mock_database.objects.filter.return_value.delete.assert_called_once()
    assert result == "BlockID 123 removed from block list."

def test_toggle_block(mock_database):
    mock_entry = MagicMock(isBlocking=True)
    mock_database.objects.get.return_value = mock_entry

    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        manager = WebsiteBlockingManager()
        result = manager.toggleBlock(123)

    assert result == "BlockID 123 toggled to not blocking."
    assert mock_entry.isBlocking is False
    mock_entry.save.assert_called_once()

def test_set_block(mock_database):
    mock_entry = MagicMock()
    mock_database.objects.get.return_value = mock_entry

    with patch.object(UserManager, "getCurrentUserID", return_value=1):
        manager = WebsiteBlockingManager()
        result = manager.setBlock(123, True)

    assert result == "BlockID 123 set to blocking."
    assert mock_entry.isBlocking is True
    mock_entry.save.assert_called_once()
