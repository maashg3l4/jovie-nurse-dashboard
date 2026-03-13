import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .data import NURSING_TIPS, NURSE_QUOTES, SELF_CARE_ITEMS, MEDICAL_ABBREVIATIONS, VITAL_SIGNS_NORMAL
from .models import VitalSign, JournalEntry, StressLog, SelfCareLog, DailyRoutine, LoveLetter

# ═══════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════
def dashboard(request):
    # Get records from database
    all_vitals = VitalSign.objects.all()[:10]
    all_journals = JournalEntry.objects.all()[:10]
    all_stress = StressLog.objects.all()[:10]
    all_routines_morning = DailyRoutine.objects.filter(routine_type='morning')
    all_routines_study = DailyRoutine.objects.filter(routine_type='study')
    all_routines_night = DailyRoutine.objects.filter(routine_type='night')

    context = {
        'tip': random.choice(NURSING_TIPS),
        'quote': random.choice(NURSE_QUOTES),
        'self_care': SELF_CARE_ITEMS,
        'abbreviations': MEDICAL_ABBREVIATIONS,
        'vitals_normal': VITAL_SIGNS_NORMAL,
        # Database history
        'all_vitals': all_vitals,
        'all_journals': all_journals,
        'all_stress': all_stress,
        'routines_morning': all_routines_morning,
        'routines_study': all_routines_study,
        'routines_night': all_routines_night,
    }
    return render(request, 'nurse/dashboard.html', context)

# ═══════════════════════════════════════
# SAVE VITALS — NOW SAVES FOREVER! 💙
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_vitals(request):
    try:
        data = json.loads(request.body)
        vital = VitalSign.objects.create(
            label=data.get('label', 'Vitals Check'),
            bp=data.get('readings', {}).get('BP', ''),
            hr=data.get('readings', {}).get('HR', ''),
            temp=data.get('readings', {}).get('TEMP', ''),
            spo2=data.get('readings', {}).get('SPO2', ''),
            bgl=data.get('readings', {}).get('BGL', ''),
            rr=data.get('readings', {}).get('RR', ''),
            notes=data.get('notes', ''),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Vitals saved forever! 💙',
            'id': vital.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# GET VITALS HISTORY
# ═══════════════════════════════════════
def get_vitals(request):
    vitals = VitalSign.objects.all()[:20]
    data = []
    for v in vitals:
        data.append({
            'id': v.id,
            'label': v.label,
            'date_time': v.date_time.strftime('%Y-%m-%d %H:%M'),
            'bp': v.bp,
            'hr': v.hr,
            'temp': v.temp,
            'spo2': v.spo2,
            'bgl': v.bgl,
            'rr': v.rr,
            'notes': v.notes,
        })
    return JsonResponse({'status': 'ok', 'vitals': data})

# ═══════════════════════════════════════
# SAVE JOURNAL — NOW SAVES FOREVER! 💙
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_journal(request):
    try:
        data = json.loads(request.body)
        entry = JournalEntry.objects.create(
            sleep_hours=float(data.get('sleep', '7').replace('h', '')),
            energy=data.get('energy', ''),
            water_glasses=int(data.get('water', 8)),
            nutrition=data.get('nutrition', ''),
            feelings=data.get('feelings', ''),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Journal saved forever! 💙',
            'id': entry.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# GET JOURNAL HISTORY
# ═══════════════════════════════════════
def get_journal(request):
    entries = JournalEntry.objects.all()[:20]
    data = []
    for e in entries:
        data.append({
            'id': e.id,
            'date': e.date.strftime('%Y-%m-%d'),
            'sleep_hours': e.sleep_hours,
            'energy': e.energy,
            'water_glasses': e.water_glasses,
            'nutrition': e.nutrition,
            'feelings': e.feelings,
        })
    return JsonResponse({'status': 'ok', 'entries': data})

# ═══════════════════════════════════════
# SAVE STRESS — NOW SAVES FOREVER! 💙
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_stress(request):
    try:
        data = json.loads(request.body)
        log = StressLog.objects.create(
            groupmates_level=int(data.get('gm', 0)),
            groupmates_note=data.get('gmNote', ''),
            overall_level=int(data.get('overall', 3)),
            notes=data.get('notes', ''),
            what_helped=data.get('helped', ''),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Stress log saved forever! 💙',
            'id': log.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# GET STRESS HISTORY
# ═══════════════════════════════════════
def get_stress(request):
    logs = StressLog.objects.all()[:20]
    data = []
    for l in logs:
        data.append({
            'id': l.id,
            'date': l.date.strftime('%Y-%m-%d'),
            'groupmates_level': l.groupmates_level,
            'groupmates_note': l.groupmates_note,
            'overall_level': l.overall_level,
            'notes': l.notes,
            'what_helped': l.what_helped,
        })
    return JsonResponse({'status': 'ok', 'logs': data})

# ═══════════════════════════════════════
# SAVE SELF CARE — NOW SAVES FOREVER! 💙
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_selfcare(request):
    try:
        data = json.loads(request.body)
        log = SelfCareLog.objects.create(
            completed_items=json.dumps(data.get('completed', [])),
            total_completed=int(data.get('total', 0)),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Self care saved forever! 💙',
            'id': log.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# SAVE ROUTINE — NOW SAVES FOREVER! 💙
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_routine(request):
    try:
        data = json.loads(request.body)
        routine = DailyRoutine.objects.create(
            routine_type=data.get('type', 'morning'),
            task_name=data.get('task', ''),
            is_completed=data.get('completed', False),
            order=data.get('order', 0),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Routine saved! 💙',
            'id': routine.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# GET ROUTINES
# ═══════════════════════════════════════
def get_routines(request):
    routines = DailyRoutine.objects.filter(
        date=timezone.now().date()
    )
    data = []
    for r in routines:
        data.append({
            'id': r.id,
            'type': r.routine_type,
            'task': r.task_name,
            'completed': r.is_completed,
            'order': r.order,
        })
    return JsonResponse({'status': 'ok', 'routines': data})

# ═══════════════════════════════════════
# TOGGLE ROUTINE COMPLETE
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def toggle_routine(request):
    try:
        data = json.loads(request.body)
        routine = DailyRoutine.objects.get(id=data.get('id'))
        routine.is_completed = not routine.is_completed
        routine.save()
        return JsonResponse({
            'status': 'ok',
            'completed': routine.is_completed
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# ═══════════════════════════════════════
# LOVE LETTER
# ═══════════════════════════════════════
def get_love_letter(request):
    from datetime import date
    today = date.today()
    unlock_date = date(2026, 3, 22)
    days_remaining = (unlock_date - today).days

    try:
        letter = LoveLetter.objects.first()
        content = letter.content if letter else ""
    except:
        content = ""

    if today >= unlock_date:
        return JsonResponse({
            'status': 'unlocked',
            'content': content,
            'message': 'Your letter is here my love 💌'
        })
    else:
        return JsonResponse({
            'status': 'locked',
            'days_remaining': days_remaining,
            'message': f'Your letter opens in {days_remaining} days 💙'
        })