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
    # Test the API
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)
    assert 'userID' not in data


@pytest.mark.django_db
def test_api_section_add(client, authenticationToken):
    # Setup
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the API
    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID": itemID
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)
    assert 'userID' not in data


@pytest.mark.django_db
def test_api_task_add(client, authenticationToken):
    # Setup project
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]
    # Setup section
    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID": itemID
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the API
    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": itemID,
        "priority": "High"
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID',
                    'dueDate', 'priority', 'status', 'description', 'inTodayDate']
    assert all(key in data for key in expectedKeys)
    assert 'userID' not in data
    assert 'taskID' not in data


@pytest.mark.django_db
def test_api_todo_item_get(client, authenticationToken):
    # Setup
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the API
    url = "/todolist/api/todo_item/get"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "itemID": itemID,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = jsonData['data']
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)
    assert 'userID' not in data
