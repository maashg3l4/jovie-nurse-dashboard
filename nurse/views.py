import json, random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .data import NURSING_TIPS, NURSE_QUOTES, SELF_CARE_ITEMS, MEDICAL_ABBREVIATIONS, VITAL_SIGNS_NORMAL

def dashboard(request):
    context = {
        'tip': random.choice(NURSING_TIPS),
        'quote': random.choice(NURSE_QUOTES),
        'self_care': SELF_CARE_ITEMS,
        'abbreviations': MEDICAL_ABBREVIATIONS,
        'vitals_normal': VITAL_SIGNS_NORMAL,
    }
    return render(request, 'nurse/dashboard.html', context)

@csrf_exempt
@require_POST
def save_journal(request):
    try:
        data = json.loads(request.body)
        return JsonResponse({'status': 'ok', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def save_vitals(request):
    try:
        data = json.loads(request.body)
        return JsonResponse({'status': 'ok', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def save_stress(request):
    try:
        data = json.loads(request.body)
        return JsonResponse({'status': 'ok', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
