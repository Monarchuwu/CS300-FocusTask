import pytest
import json
from todolist.models.managers import UserManager


@pytest.fixture
def userManager():
    return UserManager()


@pytest.mark.django_db
def test_api_user_register(client):
    url = "/todolist/api/user/register"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    }))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'


@pytest.mark.django_db
def test_api_user_signin(client, userManager):
    userManager.registerUser(
        username="testuser",
        email="test@gmail.com",
        password="password123",
    )

    url = "/todolist/api/user/signin"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "email": "test@gmail.com",
        "password": "password123"
    }))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'
    
    data = jsonData['data']
    assert 'authenticationToken' in data


@pytest.mark.django_db
def test_api_user_signout(client, userManager):
    userManager.registerUser(
        username="testuser",
        email="test@gmail.com",
        password="password123",
    )
    authenticationToken = userManager.signIn(
        email="test@gmail.com",
        password="password123"
    )

    url = "/todolist/api/user/signout"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken
    }))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'
