import pytest
from unittest.mock import patch, MagicMock
from todolist.models.managers import UserManager
from todolist.models import databases
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import bcrypt


@pytest.fixture
def user_manager():
    return UserManager()


@pytest.mark.django_db
def test_register_user_success(user_manager):
    result = user_manager.registerUser(
        username="testuser",
        email="test@example.com",
        password="password123",
        avatarURL=None
    )
    assert result == "User registered successfully"


@pytest.mark.django_db
def test_register_user_email_exists(user_manager):
    result = user_manager.registerUser(
        username="testuser",
        email="test@example.com",
        password="password123",
        avatarURL=None
    )
    assert result == "User registered successfully"

    try:
        user_manager.registerUser(
            username="testuser",
            email="test@example.com",
            password="password123",
            avatarURL=None
        )
    except ValueError as e:
        assert str(e) == "An error occurred while registering the new user: Error: Email already exists"
        return
    assert False, "Expected ValueError not raised"


@patch('todolist.models.databases.UserDB')
def test_sign_in_success(MockUserDB, user_manager):
    mock_user = MagicMock()
    mock_user.passwordHash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    mock_user.userID = 1
    MockUserDB.objects.get.return_value = mock_user

    result = user_manager.signIn(email="test@example.com", password="password123")
    assert result == "Sign-in successful"
    assert user_manager.getCurrentUserID() == 1


@patch('todolist.models.databases.UserDB')
def test_sign_in_incorrect_password(MockUserDB, user_manager):
    mock_user = MagicMock()
    mock_user.passwordHash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    MockUserDB.objects.get.return_value = mock_user

    with pytest.raises(ValueError, match="Error: Incorrect password"):
        user_manager.signIn(email="test@example.com", password="wrongpassword")


@patch('todolist.models.databases.UserDB')
def test_sign_in_user_not_found(MockUserDB, user_manager):
    MockUserDB.objects.get.side_effect = ObjectDoesNotExist

    with pytest.raises(ValueError, match="Error: User not found"):
        user_manager.signIn(email="nonexistent@example.com", password="password123")


def test_sign_out_success(user_manager):
    user_manager._currentUserID = 1
    result = user_manager.signOut()
    assert result == "Sign-out successful"
    assert user_manager.getCurrentUserID() is None


def test_sign_out_no_user_signed_in(user_manager):
    user_manager._currentUserID = None

    with pytest.raises(ValueError, match="Error: No user signed in"):
        user_manager.signOut()
