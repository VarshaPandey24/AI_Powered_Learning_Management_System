# core/urls.py
from django.urls import path, include
from .views import home_view, register_view, student_dashboard_view, instructor_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')), # For login, logout, etc.
    path('dashboard/student/', student_dashboard_view, name='student_dashboard'),
    path('dashboard/instructor/', instructor_dashboard_view, name='instructor_dashboard'),
]