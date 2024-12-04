from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the todolist.")

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
            
            return JsonResponse({'status': 'success', 'message': 'Task added successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
