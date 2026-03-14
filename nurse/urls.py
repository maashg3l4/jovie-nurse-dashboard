from django.urls import path
from . import views

app_name = 'nurse'

urlpatterns = [
    # ═══════════════════════════════
    # MAIN DASHBOARD
    # ═══════════════════════════════
    path('', views.dashboard, name='dashboard'),

    # ═══════════════════════════════
    # VITALS
    # ═══════════════════════════════
    path('api/vitals/save/', views.save_vitals, name='save_vitals'),
    path('api/vitals/get/', views.get_vitals, name='get_vitals'),

    # ═══════════════════════════════
    # JOURNAL
    # ═══════════════════════════════
    path('api/journal/save/', views.save_journal, name='save_journal'),
    path('api/journal/get/', views.get_journal, name='get_journal'),

    # ═══════════════════════════════
    # STRESS
    # ═══════════════════════════════
    path('api/stress/save/', views.save_stress, name='save_stress'),
    path('api/stress/get/', views.get_stress, name='get_stress'),

    # ═══════════════════════════════
    # SELF CARE
    # ═══════════════════════════════
    path('api/selfcare/save/', views.save_selfcare, name='save_selfcare'),

    # ═══════════════════════════════
    # ROUTINES
    # ═══════════════════════════════
    path('api/routine/save/', views.save_routine, name='save_routine'),
    path('api/routine/get/', views.get_routines, name='get_routines'),
    path('api/routine/toggle/', views.toggle_routine, name='toggle_routine'),

    # ═══════════════════════════════════════
# GOALS 🌟
# ═══════════════════════════════════════
path('api/goals/save/', views.save_goal, name='save_goal'),
path('api/goals/update/', views.update_goal, name='update_goal'),
path('api/goals/get/', views.get_goals, name='get_goals'),

# ═══════════════════════════════════════
# WELLNESS SUMMARY 📊
# ═══════════════════════════════════════
path('api/wellness/', views.get_wellness_summary, name='get_wellness_summary'),
]