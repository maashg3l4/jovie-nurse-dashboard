from django.urls import path
from . import views
app_name = 'nurse'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/journal/', views.save_journal, name='save_journal'),
    path('api/vitals/', views.save_vitals, name='save_vitals'),
    path('api/stress/', views.save_stress, name='save_stress'),
]
