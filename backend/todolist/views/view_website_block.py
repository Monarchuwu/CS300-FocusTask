from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def website_block_get_urls(request):
    if request.method == 'GET':
        try:
            # website_urls = ['youtube.com', 'facebook.com']
            # get the current time
            current_time = datetime.datetime.now()
            # if the seconds is less than 30, then website_urls is youtube.com, otherwise it is facebook.com
            website_urls = ['youtube.com'] if current_time.second < 30 else ['facebook.com']
            return JsonResponse({'status': 'success', 'data': {'website_urls': website_urls}})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)