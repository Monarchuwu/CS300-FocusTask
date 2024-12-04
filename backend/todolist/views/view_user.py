from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']
            avatarURL = data['avatarURL']
            UserManager().registerUser(username, email, password, avatarURL)
            
            return JsonResponse({'status': 'success', 'message': 'User added successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)