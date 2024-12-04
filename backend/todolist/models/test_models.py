import pytest
from todolist.models import databases

# create a temporary database for testing
@pytest.mark.django_db
def test_objects():
    user = databases.UserDB.objects.create(userID=1, username="test", email="a@gmail.com", passwordHash="123", avatarURL=None)
    databases.UserDB.objects.get(userID=1).get_data_object()
    assert True

def test_sum():
    assert 1 + 1 == 2