from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializer import ReactSerializer

# Create your views here.


class ReactView(APIView):

    serializer_class = ReactSerializer

    def get(self, request):
        detail = [{"name": detail.name, "detail": detail.detail}
                  for detail in React.objects.all()]
        return Response(detail)

    def post(self, request):

        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


def index(request):
    view_today = request.GET.get('view_today', 'false').lower() == 'true'

    if view_today:
        today = datetime.today().date()
        tasks = Task.objects.filter(createdDate__date=today)
    else:
        tasks = Task.objects.all()

    return render(request, "index.html", {'tasks': tasks})


def toggle_task_done(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(taskID=task_id)
            task.isDoneState = not task.isDoneState
            task.save()
            return JsonResponse({'success': True, 'isDoneState': task.isDoneState})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def add_task(request):
    if request.method == 'POST':
        try:
            taskID = request.POST.get('taskID')
            taskName = request.POST.get('taskName')
            dueDate = request.POST.get('dueDate')
            reminder = request.POST.get('reminder')
            repeatOne = request.POST.get(
                'repeatOne', 'false').lower() == 'true'
            repeatEveryDay = request.POST.get(
                'repeatEveryDay', 'false').lower() == 'true'
            repeatEveryWeek = request.POST.get(
                'repeatEveryWeek', 'false').lower() == 'true'
            description = request.POST.get('description')
            isDoneState = request.POST.get('isDoneState').lower() == 'true'
            createdDate = request.POST.get('createdDate')

            task = Task(taskID=taskID,
                        taskName=taskName,
                        dueDate=dueDate,
                        reminder=reminder,
                        repeatOne=repeatOne,
                        repeatEveryDay=repeatEveryDay,
                        repeatEveryWeek=repeatEveryWeek,
                        description=description,
                        isDoneState=isDoneState,
                        createdDate=createdDate)
            task.save()
            return JsonResponse({'success': True, 'taskID': task.taskID})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
