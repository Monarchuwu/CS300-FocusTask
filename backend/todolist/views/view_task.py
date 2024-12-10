from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from queue import Queue
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
            if parentItem.itemType == 'Project':
                raise Exception('Parent item must not be a project')
            if parentItem.userID != userID:
                raise Exception('User does not have permission to access this parent item')

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemID = data['itemID']
            name = data.get('name')
            parentID = data.get('parentID')

            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(itemID = itemID)

            if (userID != todoItem.userID):
                raise Exception('User does not have permission to access this item') 

            todoItem.name = name if (name is not None) else todoItem.name
            todoItem.parentID = parentID if (parentID is not None) else todoItem.parentID
            
            TaskManager().editTodoItem(todoItem=todoItem)

            return JsonResponse({'status': 'success', 'data': todoItem.to_json_without_userID()})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def task_attributes_update(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            taskID = data['taskID']
            dueDate = data.get('dueDate')
            priority = data.get('priority')
            status = data.get('status')
            description = data.get('description')
            inTodayDate = data.get('inTodayDate')


            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(itemID = taskID)
            taskAttrs = TaskManager().getTaskAttributes(taskID = taskID)

            if (userID != todoItem.userID):
                raise Exception('User does not have permission to access this item')
            
            taskAttrs.dueDate = dueDate if (dueDate is not None) else taskAttrs.dueDate
            taskAttrs.priority = priority if (priority is not None) else taskAttrs.priority
            taskAttrs.status = status if (status is not None) else taskAttrs.status
            taskAttrs.description = description if (description is not None) else taskAttrs.description
            taskAttrs.inTodayDate = datetime.fromisoformat(inTodayDate) if (inTodayDate is not None) else taskAttrs.inTodayDate

            TaskManager().deteleTaskAttributes(taskID = taskID)
            TaskManager().addTaskAttributes(attrs=taskAttrs)

            return JsonResponse({'status': 'success', 'data': str(taskAttrs)})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def todo_item_get_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemID = data['itemID']

            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(itemID = itemID)
            if (userID != todoItem.userID):
                raise Exception('User does not have permission to access this item') 

            while todoItem.itemType != 'Project' and todoItem.parentID is not None:
                todoItem = TaskManager().getTodoItem(itemID=todoItem.parentID)
                if (userID != todoItem.userID):
                    raise Exception('User does not have permission to access this item') 

            
         

            return JsonResponse({'status': 'success', 'data': todoItem.to_json_without_userID()})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            taskID = data['taskID']
            
            userID = UserManager().getUserID(token)
            todoItem = TaskManager().getTodoItem(taskID)
            if todoItem.userID != userID:
                raise Exception('User does not have permission to access this item')
            taskAttributes = TaskManager().getTaskAttributes(taskID)

            return JsonResponse({'status': 'success', 'data': str(taskAttributes)})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def todo_item_get_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemID = data['itemID']

            userID = UserManager().getUserID(token)
            queue = Queue() 
            queue.put(itemID)

            item_list = []
            while not queue.empty():
                tmpID = queue.get()

                todoItem = TaskManager().getTodoItem(itemID = tmpID)
                item_list.append(todoItem.to_json_without_userID())
                if (userID != todoItem.userID):
                    raise Exception('User does not have permission to access this item') 

                taskLists = TaskManager().getTaskList(projectID=tmpID)
                for task in taskLists:
                    queue.put(task.itemID)

            return JsonResponse({'status': 'success', 'data': item_list})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def todo_item_get_all(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']

            userID = UserManager().getUserID(token)
            itemList = TaskManager().getAllTodoItem(userID = userID)
            itemList = [item.to_json_without_userID() for item in itemList]

            return JsonResponse({'status': 'success', 'data': itemList})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def task_get_today_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']

            userID = UserManager().getUserID(token)
            today_task_list = TaskManager().getTodayTaskList()
            today_list = []

            for attrs in today_task_list:
                item = TaskManager().getTodoItem(itemID=attrs.taskID)
                if item.userID != userID or item.itemType != 'Task':
                    continue
                today_list.append(item.to_json_without_userID())

            return JsonResponse({'status': 'success', 'data': today_list})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def task_attributes_get_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            itemIDs = data['itemIDs']

            userID = UserManager().getUserID(token)
            
            task_attributes_list = []

            for itemID in itemIDs:
                task = TaskManager().getTodoItem(itemID = itemID)
                if (task.itemType != 'Task'):
                    continue
                if task.userID != userID:
                    raise Exception('User does not have permission to access this item')

                taskAttrs = TaskManager().getTaskAttributes(taskID = itemID)
                task_attributes_list.append(str(taskAttrs))

            return JsonResponse({'status': 'success', 'data': task_attributes_list})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
