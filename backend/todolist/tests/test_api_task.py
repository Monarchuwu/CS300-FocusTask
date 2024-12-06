import pytest
import json
from todolist.models.managers import UserManager


@pytest.fixture
def userManager():
    return UserManager()

@pytest.fixture
def authenticationToken(userManager):
    userManager.registerUser(
        username="testuser",
        email="test@gmail.com",
        password="password123",
    )
    return userManager.signIn(
        email="test@gmail.com",
        password="password123"
    )


@pytest.mark.django_db
def test_api_project_add(client, authenticationToken):
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))

    print(response.json())
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = jsonData['data']
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)


@pytest.mark.django_db
def test_api_section_add(client, authenticationToken):
    return

    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))

    print(response.json())
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = jsonData['data']
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)

@pytest.mark.django_db
def test_api_todo_item_get(client, authenticationToken):
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    print(response.json())
    itemID = response.json()['data']["itemID"]

    url = "/todolist/api/todo_item/get"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "itemID": itemID,
    }))

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = jsonData['data']
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)