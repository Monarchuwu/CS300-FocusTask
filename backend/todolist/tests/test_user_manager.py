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


@pytest.mark.django_db
def test_sign_in_success(user_manager):
    user_manager.registerUser(
        username="testuser",
        email="test@example.com",
        password="password123",
        avatarURL=None
    )
    authenticationToken = user_manager.signIn(email="test@example.com", password="password123")

    try:
        databases.AuthenticationTokenDB.objects.get(tokenValue=authenticationToken)
    except databases.AuthenticationTokenDB.DoesNotExist:
        assert False, "Authentication token not created in the database"


@pytest.mark.django_db
def test_sign_in_incorrect_password(user_manager):
    user_manager.registerUser(
        username="testuser",
        email="test@example.com",
        password="password123",
        avatarURL=None
    )
    try:
        user_manager.signIn(email="test@example.com", password="password123")
    except ValueError as e:
        assert str(e) == "Error: Incorrect password"


@pytest.mark.django_db
def test_sign_in_user_not_found(user_manager):
    try:
        user_manager.signIn(email="test@example.com", password="password123")
    except ValueError as e:
        assert str(e) == "Error: User not found"


@pytest.mark.django_db
def test_sign_out_success(user_manager):
    user_manager.registerUser(
        username="testuser",
        email="test@example.com",
        password="password123",
        avatarURL=None
    )
    authenticationToken = user_manager.signIn(email="test@example.com", password="password123")
    result = user_manager.signOut(authenticationToken)
    assert result == "User signed out successfully"
    

@pytest.mark.django_db
def test_sign_out_no_user_signed_in(user_manager):
    try:
        user_manager.signOut("fake_token")
    except ValueError as e:
        assert str(e) == "Error: Authentication token not found"