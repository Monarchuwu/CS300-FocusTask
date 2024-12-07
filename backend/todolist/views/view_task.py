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
            
            return JsonResponse({'status': 'success', 'data': todoItem.to_json_without_userID()})
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
            
            return JsonResponse({'status': 'success', 'data': todoItem.to_json_without_userID()})
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
            token = data['authenticationToken']
            name = data['name']
            parentID = data['parentID']
            userID = UserManager().getUserID(token)

            if parentID is None:
                raise Exception('Parent ID cannot be None')
            parentItem = TaskManager().getTodoItem(parentID)
            if parentItem.itemType != 'Section':
                raise Exception('Parent item must be a section')
            if parentItem.userID != userID:
                raise Exception('User does not have permission to access this section')

            # Create a new todo item object
            todoItem = TodoItem(
                itemID = None,
                name = name,
                parentID = parentID,
                createdDate = None,
                userID = userID,
                itemType = 'Task',
                labelID = None
            )
            todoItem = TaskManager().addTodoItem(todoItem)

            # Create a new task attributes object
            attributes = {}
            for key in ['dueDate', 'priority', 'status', 'description', 'inTodayDate']:
                if key in data:
                    attributes[key] = data[key]
            taskAttributes = TaskAttributes(
                taskID = todoItem.itemID,
                **attributes
            )
            taskAttributes = TaskManager().addTaskAttributes(taskAttributes)

            # Response data
            data = json.dumps({
                **json.loads(todoItem.to_json_without_userID()),
                **json.loads(taskAttributes.to_json_without_taskID())
            })

            return JsonResponse({'status': 'success', 'data': data})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def todo_item_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemID = data['itemID']
            
            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(itemID)
            if todoItem.userID != userID:
                raise Exception('User does not have permission to access this item')
            
            if todoItem.itemType == 'Task':
                TaskManager().deteleTaskAttributes(itemID)
            TaskManager().deleteTodoItem(itemID)

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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
            
            return JsonResponse({'status': 'success', 'data': todoItem.to_json_without_userID()})
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
