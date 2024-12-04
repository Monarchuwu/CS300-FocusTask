from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            return JsonResponse({'status': 'success', 'message': f'The message is {message}'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
