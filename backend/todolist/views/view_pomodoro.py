from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pomodoro_start(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkRunningPomodoro(userID):
                return JsonResponse({'status': 'error', 'message': 'User is not allowed to start more than one session'}, status = 409) 
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                pomodoro = PomodoroManager().start(pomodoroID=pomodoroID)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_pause(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                pomodoro = PomodoroManager().pause(pomodoroID=pomodoroID)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_continue(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                pomodoro = PomodoroManager().unpause(pomodoroID=pomodoroID)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_end(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                pomodoro = PomodoroManager().end(pomodoroID=pomodoroID)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_set_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            taskID = data['taskID']
            todoItem = TaskManager().getTodoItem(itemID = taskID)
            userID = UserManager().getUserID(token)
            if todoItem.userID == userID:
                pomodoro = PomodoroManager().setTaskID(taskID=taskID)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_set_length(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            seconds = data['length']
            length=timedelta(seconds=seconds)
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                pomodoro = PomodoroManager().setTime(pomodoroID=pomodoroID, length=length)
                return JsonResponse({'status': 'success', 'data': str(pomodoro)})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def pomodoro_get_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            pomodoroID = data['pomodoroID']
            userID = UserManager().getUserID(token)
            if PomodoroManager().checkUserAccessToPomodoro(userID, pomodoroID):
                currentTime = PomodoroManager().getTime(pomodoroID=pomodoroID)
                return JsonResponse({'status': 'success', 'data': currentTime.total_seconds()})
            else:
                return JsonResponse({'status': 'error', 'message': 'User is unauthorized to modify this session'}, status = 401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_history_hour(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            time = datetime.fromisoformat(data['hour'])
            time = datetime(year=time.year, month=time.month, day=time.day, hour=time.hour).astimezone()
            userID = UserManager().getUserID(token)
            
            run_time, pause_time = PomodoroManager().get_hour_list(userID, time)
            return JsonResponse({'status': 'success', 'data': [run_time, pause_time]})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_history_hour_fullday(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            time = datetime.fromisoformat(data['date']).replace(hour=0, minute=0, second=0, microsecond=0)
            userID = UserManager().getUserID(token)
            result = []
            for hour in range(24):
                run_time, pause_time = PomodoroManager().get_hour_list(userID, time + timedelta(hours=hour))
                result.append([run_time, pause_time])

            return JsonResponse({'status': 'success', 'data': result})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_history_day(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            time = datetime.fromisoformat(data['hour']).date()
            userID = UserManager().getUserID(token)
            
            run_time, pause_time = PomodoroManager().get_day_list(userID, time)
            return JsonResponse({'status': 'success', 'data': [run_time, pause_time]})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_last_active_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            pomodoro = PomodoroManager().getLastActiveSession(userID)

            if pomodoro is None:
                return JsonResponse({'status': 'success', 'data': json.dumps({ 'haveActiveSession': False })})
            
            return JsonResponse({'status': 'success', 'data': json.dumps({
                'haveActiveSession': True,
                'pomodoro': json.loads(str(pomodoro))
            })})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)