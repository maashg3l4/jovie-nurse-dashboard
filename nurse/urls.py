from django.urls import path
from . import views

app_name = 'nurse'

urlpatterns = [
    # MAIN DASHBOARD
    path('', views.dashboard, name='dashboard'),

    # VITALS
    path('api/vitals/save/', views.save_vitals, name='save_vitals'),
    path('api/vitals/get/', views.get_vitals, name='get_vitals'),

    # JOURNAL
    path('api/journal/save/', views.save_journal, name='save_journal'),
    path('api/journal/get/', views.get_journal, name='get_journal'),

    # STRESS
    path('api/stress/save/', views.save_stress, name='save_stress'),
    path('api/stress/get/', views.get_stress, name='get_stress'),

    # SELF CARE
    path('api/selfcare/save/', views.save_selfcare, name='save_selfcare'),

    # ROUTINES
    path('api/routine/save/', views.save_routine, name='save_routine'),
    path('api/routine/get/', views.get_routines, name='get_routines'),
    path('api/routine/toggle/', views.toggle_routine, name='toggle_routine'),
    path('api/routine/delete/', views.delete_routine, name='delete_routine'),
    path('api/routine/check/', views.update_routine_check, name='update_routine_check'),

    # GOALS
    path('api/goals/save/', views.save_goal, name='save_goal'),
    path('api/goals/update/', views.update_goal, name='update_goal'),
    path('api/goals/get/', views.get_goals, name='get_goals'),

    # WELLNESS
    path('api/wellness/', views.get_wellness_summary, name='get_wellness_summary'),

    # LOVE LETTER 💌
    path('api/letter/', views.get_love_letter, name='get_love_letter'),

    # PERIOD TRACKER 🌸
    path('api/period/save/', views.save_period_log, name='save_period_log'),
    path('api/period/get/', views.get_period_logs, name='get_period_logs'),
    path('api/cycle/save/', views.save_cycle_info, name='save_cycle_info'),
    path('api/cycle/get/', views.get_cycle_info, name='get_cycle_info'),
]