import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .data import NURSING_TIPS, NURSE_QUOTES, SELF_CARE_ITEMS, MEDICAL_ABBREVIATIONS, VITAL_SIGNS_NORMAL
from .models import VitalSign, JournalEntry, StressLog, SelfCareLog, DailyRoutine, LoveLetter, Goal, WellnessSummary, PeriodLog, CycleInfo

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
        # Goals
        'goals_nursing': Goal.objects.filter(category='nursing').order_by('target_date'),
        'goals_personal': Goal.objects.filter(category='personal').order_by('target_date'),
        'goals_relationship': Goal.objects.filter(category='relationship').order_by('target_date'),
        'goals_todo': Goal.objects.filter(status='todo').order_by('target_date'),
        'goals_inprogress': Goal.objects.filter(status='inprogress').order_by('target_date'),
        'goals_done': Goal.objects.filter(status='done').order_by('target_date'),
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
            'id': routine.id,
            'task': routine.task_name,
            'type': routine.routine_type,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_POST
def delete_routine(request):
    try:
        data = json.loads(request.body)
        DailyRoutine.objects.filter(id=data.get('id')).delete()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def update_routine_check(request):
    try:
        data = json.loads(request.body)
        routine = DailyRoutine.objects.get(id=data.get('id'))
        routine.is_completed = data.get('completed', False)
        routine.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# ═══════════════════════════════════════
# GET ROUTINES
# ═══════════════════════════════════════
def get_routines(request):
    routine_type = request.GET.get('type', None)
    if routine_type:
        routines = DailyRoutine.objects.filter(routine_type=routine_type)
    else:
        routines = DailyRoutine.objects.all()
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
    try:
        letter = LoveLetter.objects.first()
        if letter:
            return JsonResponse({
                'status': 'unlocked',
                'content': letter.content,
                'message': 'Your letter is here my love 💌'
            })
        else:
            return JsonResponse({
                'status': 'unlocked',
                'content': 'My Dearest Angela... 💙',
                'message': 'Your letter is here my love 💌'
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
        
        # ═══════════════════════════════════════
# GOALS API
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_goal(request):
    try:
        data = json.loads(request.body)
        goal = Goal.objects.create(
            title=data.get('title', ''),
            category=data.get('category', 'personal'),
            status=data.get('status', 'todo'),
            target_date=data.get('target_date', None),
            total_steps=int(data.get('total_steps', 5)),
            completed_steps=int(data.get('completed_steps', 0)),
            notes=data.get('notes', ''),
        )
        return JsonResponse({
            'status': 'ok',
            'message': 'Goal saved forever! 💙',
            'id': goal.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_POST
def update_goal(request):
    try:
        data = json.loads(request.body)
        goal = Goal.objects.get(id=data.get('id'))
        if 'status' in data:
            goal.status = data['status']
        if 'completed_steps' in data:
            goal.completed_steps = int(data['completed_steps'])
        if 'notes' in data:
            goal.notes = data['notes']
        goal.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'Goal updated! 💙',
            'progress': goal.progress_percentage()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_goals(request):
    goals = Goal.objects.all()
    data = []
    for g in goals:
        data.append({
            'id': g.id,
            'title': g.title,
            'category': g.category,
            'status': g.status,
            'target_date': g.target_date.strftime('%Y-%m-%d') if g.target_date else '',
            'total_steps': g.total_steps,
            'completed_steps': g.completed_steps,
            'progress': g.progress_percentage(),
            'notes': g.notes,
        })
    return JsonResponse({'status': 'ok', 'goals': data})

# ═══════════════════════════════════════
# WELLNESS SUMMARY
# ═══════════════════════════════════════
def get_wellness_summary(request):
    from django.utils import timezone
    from django.db.models import Avg, Count, Sum
    import datetime

    # Get period from request
    period = request.GET.get('period', 'month')
    now = timezone.now()

    if period == 'month':
        start_date = now.replace(day=1).date()
    elif period == 'week':
        start_date = (now - datetime.timedelta(days=7)).date()
    else:
        start_date = (now - datetime.timedelta(days=30)).date()

    # Calculate stats
    journals = JournalEntry.objects.filter(date__gte=start_date)
    vitals = VitalSign.objects.filter(date_time__date__gte=start_date)
    stress_logs = StressLog.objects.filter(date__gte=start_date)
    selfcare_logs = SelfCareLog.objects.filter(date__gte=start_date)

    avg_sleep = journals.aggregate(Avg('sleep_hours'))['sleep_hours__avg'] or 0
    total_water = journals.aggregate(Sum('water_glasses'))['water_glasses__sum'] or 0
    avg_stress = stress_logs.aggregate(Avg('overall_level'))['overall_level__avg'] or 0
    vitals_count = vitals.count()
    journal_count = journals.count()
    selfcare_count = selfcare_logs.count()

    return JsonResponse({
        'status': 'ok',
        'period': period,
        'start_date': str(start_date),
        'stats': {
            'avg_sleep': round(avg_sleep, 1),
            'total_water': total_water,
            'avg_stress': round(avg_stress, 1),
            'vitals_count': vitals_count,
            'journal_count': journal_count,
            'selfcare_count': selfcare_count,
        }
    })
    # ═══════════════════════════════════════
# 🌸 PERIOD TRACKER / MONTHLY WELLNESS
# ═══════════════════════════════════════
@csrf_exempt
@require_POST
def save_period_log(request):
    try:
        data = json.loads(request.body)
        log = PeriodLog.objects.create(
            date=data.get('date', timezone.now().date()),
            phase=data.get('phase', 'regular'),
            flow=data.get('flow', ''),
            pain_level=int(data.get('pain_level', 0)),
            mood=data.get('mood', ''),
            symptoms=json.dumps(data.get('symptoms', [])),
            notes=data.get('notes', ''),
            medication_taken=data.get('medication_taken', False),
            water_reminder=data.get('water_reminder', False),
        )
        # Update cycle info
        if data.get('phase') == 'period':
            cycle, created = CycleInfo.objects.get_or_create(id=1)
            if data.get('is_start'):
                from datetime import date, timedelta
                start = date.fromisoformat(data.get('date'))
                cycle.last_period_start = start
                cycle.next_period_prediction = start + timedelta(days=cycle.cycle_length)
                cycle.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'Period log saved! 💙',
            'id': log.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_period_logs(request):
    logs = PeriodLog.objects.all()[:30]
    data = []
    for l in logs:
        data.append({
            'id': l.id,
            'date': l.date.strftime('%Y-%m-%d'),
            'phase': l.phase,
            'flow': l.flow,
            'pain_level': l.pain_level,
            'mood': l.mood,
            'symptoms': json.loads(l.symptoms) if l.symptoms else [],
            'notes': l.notes,
            'medication_taken': l.medication_taken,
        })
    return JsonResponse({'status': 'ok', 'logs': data})

@csrf_exempt
@require_POST
def save_cycle_info(request):
    try:
        data = json.loads(request.body)
        from datetime import date, timedelta
        cycle, created = CycleInfo.objects.get_or_create(id=1)
        if data.get('last_period_start'):
            cycle.last_period_start = date.fromisoformat(data['last_period_start'])
        if data.get('last_period_end'):
            cycle.last_period_end = date.fromisoformat(data['last_period_end'])
        if data.get('cycle_length'):
            cycle.cycle_length = int(data['cycle_length'])
        if data.get('period_length'):
            cycle.period_length = int(data['period_length'])
        # Calculate next period
        if cycle.last_period_start:
            cycle.next_period_prediction = cycle.last_period_start + timedelta(days=cycle.cycle_length)
        cycle.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'Cycle info saved! 💙',
            'next_period': str(cycle.next_period_prediction) if cycle.next_period_prediction else None
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_cycle_info(request):
    try:
        cycle = CycleInfo.objects.get(id=1)
        return JsonResponse({
            'status': 'ok',
            'last_period_start': str(cycle.last_period_start) if cycle.last_period_start else None,
            'last_period_end': str(cycle.last_period_end) if cycle.last_period_end else None,
            'cycle_length': cycle.cycle_length,
            'period_length': cycle.period_length,
            'next_period': str(cycle.next_period_prediction) if cycle.next_period_prediction else None,
        })
    except CycleInfo.DoesNotExist:
        return JsonResponse({
            'status': 'ok',
            'last_period_start': None,
            'last_period_end': None,
            'cycle_length': 28,
            'period_length': 5,
            'next_period': None,
        })