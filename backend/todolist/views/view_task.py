from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def project_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            name = data['name']
            userID = UserManager().getUserID(token)
            # Create a new todo item object
            todoItem = TodoItem(
                itemID = None,
                name = name,
                parentID = None,
                createdDate = None,
                userID = userID,
                itemType = 'Project',
                labelID = None
            )
            todoItem = TaskManager().addTodoItem(todoItem)
            
            return JsonResponse({'status': 'success', 'data': str(todoItem)})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def section_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            name = data['name']
            parentID = data['parentID']
            userID = UserManager().getUserID(token)

            if parentID is None:
                raise Exception('Parent ID cannot be None')            
            parentItem = TaskManager().getTodoItem(parentID)
            if parentItem.itemType != 'Project':
                raise Exception('Parent item must be a project')
            if parentItem.userID != userID:
                raise Exception('User does not have permission to access this project')

            # Create a new todo item object
            todoItem = TodoItem(
                itemID = None,
                name = name,
                parentID = parentID,
                createdDate = None,
                userID = userID,
                itemType = 'Section',
                labelID = None
            )
            todoItem = TaskManager().addTodoItem(todoItem)
            
            return JsonResponse({'status': 'success', 'data': str(todoItem)})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def task_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create a new task object
            task = TodoItem.from_json(data)
            # return JsonResponse({'status': 'success', 'item': str(task)})
            # # Add the task to the database
            task_manager = TaskManager()
            task_manager.addTask(task)
            
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def todo_item_delete(request):
    pass

@csrf_exempt
def todo_item_update(request):
    pass

@csrf_exempt
def task_attributes_update(request):
    pass

@csrf_exempt
def todo_item_get_project(request):
    pass

@csrf_exempt
def todo_item_get(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemID = data['itemID']
            
            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(itemID)
            if todoItem.userID != userID:
                raise Exception('User does not have permission to access this item')
            
            return JsonResponse({'status': 'success', 'data': str(todoItem)})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def task_attributes_get(request):
    pass

@csrf_exempt
def todo_item_get_list(request):
    pass

@csrf_exempt
def task_get_today_list(request):
    pass

@csrf_exempt
def task_attributes_get_list(request):
    pass
