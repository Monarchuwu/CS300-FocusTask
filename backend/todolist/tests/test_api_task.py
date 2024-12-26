from django.utils import timezone
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
def test_api_todo_item_delete(client, authenticationToken):
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
    # Setup task
    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": itemID,
    }))

    # Test the API
    url = "/todolist/api/todo_item/delete"
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


@pytest.mark.django_db
def test_api_todo_item_delete_subtree(client, authenticationToken):
    pass

@pytest.mark.django_db
def test_api_todo_item_update(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/todo_item/update"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "itemID": itemID,
        "name": "test2project",
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    jsonData = json.loads(jsonData['data'])
    assert jsonData['name'] == "test2project"
    assert jsonData['parentID'] == data['parentID']


@pytest.mark.django_db
def test_api_task_attributes_update(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":itemID,
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": itemID,
        "priority": "High",
        "description": "Nothing here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/task_attributes/update"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": itemID,
        "description": "test2project",
        "priority": "Low",
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    jsonData = json.loads(jsonData['data'])
    assert jsonData['description'] == "test2project"
    assert jsonData['priority'] == "Low"
    assert jsonData['inTodayDate'] == data['inTodayDate']


@pytest.mark.django_db
def test_api_todo_item_get_project(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    data = json.loads(response.json()['data'])
    projectID = data["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":projectID,
    }))
    data = json.loads(response.json()['data'])
    sectionID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": sectionID,
        "priority": "High",
        "description": "Nothing here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/todo_item/get_project"
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
    assert jsonData['status']=="success"

    jsonData = json.loads(jsonData['data'])
    assert jsonData['itemID'] == projectID


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

    data = json.loads(jsonData['data'])
    expectedKeys = ['itemID', 'name', 'parentID', 'createdDate', 'itemType', 'labelID']
    assert all(key in data for key in expectedKeys)
    assert 'userID' not in data


@pytest.mark.django_db
def test_api_task_attributes_get(client, authenticationToken):
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
    # Setup task
    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": itemID,
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the API
    url = "/todolist/api/task_attributes/get"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": itemID,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"
    
    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    expectedKeys = ['taskID', 'dueDate', 'priority', 'status', 'description', 'inTodayDate']
    assert all(key in data for key in expectedKeys)


@pytest.mark.django_db
def test_api_todo_item_get_list(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    project = json.loads(response.json()['data'])
    projectID = project["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":projectID,
    }))
    data = json.loads(response.json()['data'])
    sectionID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": sectionID,
        "priority": "High",
        "description": "Nothing here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/todo_item/get_list"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "itemID": projectID,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    itemList = [projectID, projectID+1, sectionID, itemID]

    jsonDatas = jsonData['data']
    # print(jsonDatas)
    assert len(jsonDatas) == len(itemList)
    for jsondata in jsonDatas:
        assert json.loads(jsondata)['itemID'] in itemList


@pytest.mark.django_db
def test_api_todo_item_get_project_list(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    project = json.loads(response.json()['data'])
    projectID = project["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":projectID,
    }))
    data = json.loads(response.json()['data'])
    sectionID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": sectionID,
        "priority": "High",
        "description": "Nothing here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/todo_item/get_project_list"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "projectName": "testproject",
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    itemList = [projectID, projectID+1, sectionID, itemID]

    jsonDatas = jsonData['data']
    # print(jsonDatas)
    assert len(jsonDatas) == len(itemList)
    for jsondata in jsonDatas:
        assert json.loads(jsondata)['itemID'] in itemList


@pytest.mark.django_db
def test_api_todo_item_get_all(client, authenticationToken):
    # Set up project
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject1",
    }))
    projectID1 = json.loads(response.json()['data'])["itemID"]
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject2",
    }))
    projectID2 = json.loads(response.json()['data'])["itemID"]

    # Test the api
    url = "/todolist/api/todo_item/get_all"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == "success"

    # projectID1-2 is the empty project of the user
    # projectID1-1 is the empty section of the empty project
    itemList = [projectID1-2, projectID1-1, projectID1, projectID1+1, projectID2, projectID2+1]
    nameList = ['', 'testproject1', 'testproject2']
    jsonDatas = jsonData['data']
    assert len(jsonDatas) == len(itemList)
    for jsondata in jsonDatas:
        assert json.loads(jsondata)['itemID'] in itemList
        assert json.loads(jsondata)['name'] in nameList


@pytest.mark.django_db
def test_api_project_get_all(client, authenticationToken):
    # Set up 2 projects
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject1",
    }))
    projectID1 = json.loads(response.json()['data'])["itemID"]
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject2",
    }))
    projectID2 = json.loads(response.json()['data'])["itemID"]

    # Test the api
    url = "/todolist/api/project/get_all"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == "success"

    # projectID1-2 is the empty project of the user
    projectList = [projectID1-2, projectID1, projectID2]
    nameList = ['', 'testproject1', 'testproject2']
    jsonDatas = jsonData['data']
    assert len(jsonDatas) == len(projectList)
    for jsondata in jsonDatas:
        assert json.loads(jsondata)['itemID'] in projectList
        assert json.loads(jsondata)['name'] in nameList


@pytest.mark.django_db
def test_api_task_get_today_list(client, authenticationToken):
    # Set up
    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    project = json.loads(response.json()['data'])
    projectID = project["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":projectID,
    }))
    data = json.loads(response.json()['data'])
    sectionID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": sectionID,
        "priority": "High",
        "description": "Nothing here",
        "inTodayDate": timezone.now(),
    }, default = str))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]

    # Test the api
    url = "/todolist/api/task/get_today_list"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    itemList = [itemID]

    jsonDatas = jsonData['data']
    # print(jsonDatas)
    assert len(jsonDatas) == len(itemList)

    for jsondata in jsonDatas:
        assert json.loads(jsondata)['itemID'] in itemList


@pytest.mark.django_db
def test_api_task_attributes_get_list(client, authenticationToken):
    # Set up
    itemList = []

    url = "/todolist/api/project/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testproject",
    }))
    project = json.loads(response.json()['data'])
    projectID = project["itemID"]

    url = "/todolist/api/section/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testsection",
        "parentID":projectID,
    }))
    data = json.loads(response.json()['data'])
    sectionID = data["itemID"]

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "testtask",
        "parentID": sectionID,
        "priority": "High",
        "description": "Nothing here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]
    itemList.append(itemID)

    url = "/todolist/api/task/add"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "name": "test2task",
        "parentID": sectionID,
        "priority": "Low",
        "description": "Something here",
    }))
    data = json.loads(response.json()['data'])
    itemID = data["itemID"]
    itemList.append(itemID)

    # Test the api
    url = "/todolist/api/task_attributes/get_list"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "itemIDs": itemList,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status']=="success"

    nameList = ['Nothing here', 'Something here']

    jsonDatas = jsonData['data']
    assert len(jsonDatas) == len(nameList)
    for jsondata in jsonDatas:
        assert json.loads(jsondata)['description'] in nameList