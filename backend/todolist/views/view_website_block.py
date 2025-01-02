from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from ..models.objects import *
from ..models.managers import *
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def website_block_get_block_list(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            block_list = WebsiteBlockingManager().getBlockList(userID)
            json_block_list = []
            for block in block_list:
                json_block_list.append(block.to_json_without_userID())
            return JsonResponse({'status': 'success', 'data': json_block_list})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def website_block_get_urls(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            website_urls = WebsiteBlockingManager().getBlockingURLs(userID)
            return JsonResponse({'status': 'success', 'data': website_urls})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def add_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            URL = data['URL']
            WebsiteBlockingManager().addToBlockList(userID, URL)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def delete_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            blockID = data['blockID']
            WebsiteBlockingManager().deleteFromBlockList(userID, blockID)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def set_block_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['authenticationToken']
            userID = UserManager().getUserID(token)
            blockID = data['blockID']
            status = data['status']
            WebsiteBlockingManager().setBlock(userID, blockID, status)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)