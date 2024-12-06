import pytest
import json
from unittest.mock import patch, MagicMock


def post_api_user_register(client, data):
    url = "/todolist/api/user/register"
    return client.post(url, data=data, content_type='application/json')

def post_api_user_signin(client, data):
    url = "/todolist/api/user/signin"
    return client.post(url, data=data, content_type='application/json')

def post_api_user_signout(client, data):
    url = "/todolist/api/user/signout"
    return client.post(url, data=data, content_type='application/json')


@pytest.mark.django_db
def test_api_user_register(client):
    payload = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    }
    response = post_api_user_register(client, json.dumps(payload))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'

@pytest.mark.django_db
def test_api_user_signin(client):
    post_api_user_register(client, json.dumps({
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    }))

    response = post_api_user_signin(client, json.dumps({
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
def test_api_user_signout(client):
    post_api_user_register(client, json.dumps({
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    }))
    response = post_api_user_signin(client, json.dumps({
        "email": "test@gmail.com",
        "password": "password123"
    }))
    authenticationToken = response.json()['data']['authenticationToken']

    response = post_api_user_signout(client, json.dumps({
        "authenticationToken": authenticationToken
    }))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'
