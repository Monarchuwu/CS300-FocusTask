from django.utils import timezone
import pytest
import json
import time_machine
from datetime import datetime, timedelta
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
def test_api_pomodoro_set_task(client, authenticationToken):
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
    taskID = data['itemID']
    # Test the API
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert taskID == data['taskID']

@pytest.mark.django_db
def test_api_pomodoro_set_length(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Test the api
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))

    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert timedelta(hours = 1).total_seconds() == data['duration']

@pytest.mark.django_db
def test_api_pomodoro_start(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Test the api
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))


    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert "Running" == data['status']
    assert data['startTime'] is not None
    assert data['currentDuration'] is not None
    assert data['endTime'] is not None
    assert data['duration'] is not None
    startTime = datetime.fromisoformat(data['startTime'])
    endTime = datetime.fromisoformat(data['endTime'])
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        assert timezone.now() == startTime
        assert startTime == endTime
        assert data['duration'] == timedelta(hours = 1).total_seconds()
        assert data['currentDuration'] == timedelta(hours = 1).total_seconds()


@pytest.mark.django_db
def test_api_pomodoro_pause(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Start the pomodoro
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Test the api
    with time_machine.travel("2024-01-01 12:30:00", tick=False):
        url = "/todolist/api/pomodoro/pause"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))


    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert "Paused" == data['status']
    assert data['startTime'] is not None
    assert data['currentDuration'] is not None
    assert data['endTime'] is not None
    assert data['duration'] is not None
    startTime = datetime.fromisoformat(data['startTime'])
    endTime = datetime.fromisoformat(data['endTime'])
    with time_machine.travel("2024-01-01 12:30:00", tick=False):
        assert timezone.now() == endTime
        assert startTime + timedelta(minutes=30) == endTime
        assert data['duration'] == timedelta(hours = 1).total_seconds()
        assert data['currentDuration'] == timedelta(minutes=30).total_seconds()

@pytest.mark.django_db
def test_api_pomodoro_continue(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Start the pomodoro
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Pause the pomodoro
    with time_machine.travel("2024-01-01 12:15:00", tick=False):
        url = "/todolist/api/pomodoro/pause"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Test the api 
    with time_machine.travel("2024-01-01 12:35:00", tick=False):
        url = "/todolist/api/pomodoro/continue"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))


    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert "Running" == data['status']
    assert data['startTime'] is not None
    assert data['currentDuration'] is not None
    assert data['endTime'] is not None
    assert data['duration'] is not None
    startTime = datetime.fromisoformat(data['startTime'])
    endTime = datetime.fromisoformat(data['endTime'])
    with time_machine.travel("2024-01-01 12:35:00", tick=False):
        assert timezone.now() == endTime
        assert startTime + timedelta(minutes=35) == endTime
        assert data['duration'] == timedelta(hours = 1).total_seconds()
        assert data['currentDuration'] == timedelta(minutes=45).total_seconds()

@pytest.mark.django_db
def test_api_pomodoro_end(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Start the pomodoro
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # End the pomodoro
    with time_machine.travel("2024-01-01 12:15:00", tick=False):
        url = "/todolist/api/pomodoro/end"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))


    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    data = json.loads(jsonData['data'])
    assert "Completed" == data['status']
    assert data['startTime'] is not None
    assert data['currentDuration'] is not None
    assert data['endTime'] is not None
    assert data['duration'] is not None
    startTime = datetime.fromisoformat(data['startTime'])
    endTime = datetime.fromisoformat(data['endTime'])
    with time_machine.travel("2024-01-01 12:15:00", tick=False):
        assert timezone.now() == endTime
        assert startTime + timedelta(minutes=15) == endTime
        assert data['duration'] == timedelta(hours = 1).total_seconds()
        assert data['currentDuration'] == timedelta().total_seconds()

@pytest.mark.django_db
def test_api_pomodoro_get_time(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Start the pomodoro
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Test the api
    with time_machine.travel("2024-01-01 12:15:00", tick=False):
        url = "/todolist/api/pomodoro/get_time"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    time = timedelta(seconds=jsonData['data'])
    assert time == timedelta(minutes=45)

    # Pause the pomodoro
    with time_machine.travel("2024-01-01 12:20:00", tick=False):
        url = "/todolist/api/pomodoro/pause"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Test the api
    with time_machine.travel("2024-01-01 12:25:00", tick=False):
        url = "/todolist/api/pomodoro/get_time"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    time = timedelta(seconds=jsonData['data'])
    assert time == timedelta(minutes=40)

    # Continue the pomodoro
    with time_machine.travel("2024-01-01 12:30:00", tick=False):
        url = "/todolist/api/pomodoro/continue"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Test the api
    with time_machine.travel("2024-01-01 12:35:00", tick=False):
        url = "/todolist/api/pomodoro/get_time"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    time = timedelta(seconds=jsonData['data'])
    assert time == timedelta(minutes=35)

    # Test the api
    with time_machine.travel("2024-01-01 13:35:00", tick=False):
        url = "/todolist/api/pomodoro/get_time"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    time = timedelta(seconds=jsonData['data'])
    assert time == timedelta(minutes=0)

@pytest.mark.django_db
def test_api_pomodoro_get_history_hour(client, authenticationToken):
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
    taskID = data['itemID']
    # Set up pomodoro
    url = "/todolist/api/pomodoro/set_task"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "taskID": taskID,
    }))
    data = json.loads(response.json()['data'])
    pomodoroID = data['pomodoroID']
    # Set up length
    url = "/todolist/api/pomodoro/set_length"
    response = client.post(url, content_type='application/json', data=json.dumps({
        "authenticationToken": authenticationToken,
        "pomodoroID": pomodoroID,
        "length" : timedelta(hours=1).total_seconds()
    }))
    # Start the pomodoro
    with time_machine.travel("2024-01-01 12:00:00", tick=False):
        url = "/todolist/api/pomodoro/start"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))

    # Pause the pomodoro
    with time_machine.travel("2024-01-01 12:20:00", tick=False):
        url = "/todolist/api/pomodoro/pause"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    
    # Continue the pomodoro
    with time_machine.travel("2024-01-01 12:30:00", tick=False):
        url = "/todolist/api/pomodoro/continue"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))

    # End the pomodoro
    with time_machine.travel("2024-01-01 12:40:00", tick=False):
        url = "/todolist/api/pomodoro/end"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "pomodoroID": pomodoroID,
        }))
    
    # Test the api
    with time_machine.travel("2024-01-01 12:45:00", tick=False):
        url = "/todolist/api/pomodoro/get_history_hour"
        response = client.post(url, content_type='application/json', data=json.dumps({
            "authenticationToken": authenticationToken,
            "hour": timezone.now().isoformat(),
        }))
    # Check the response status
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} and {response.json()['message']}"
    assert response.headers["Content-Type"] == "application/json", \
        f"Expected content-type 'application/json', but got {response.headers['Content-Type']}"

    # Check the response data
    jsonData = response.json()
    assert jsonData['status'] == 'success'

    run_time, pause_time = jsonData['data']
    assert run_time == timedelta(minutes=30).total_seconds()
    assert pause_time == timedelta(minutes=10).total_seconds()