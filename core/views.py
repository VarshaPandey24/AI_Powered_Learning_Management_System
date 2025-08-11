# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from courses.models import Course

# This is a decorator we'll create to check the user's role
from .decorators import role_required

def home_view(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if hasattr(request.user, 'profile') and request.user.profile.role == 'instructor':
            return redirect('instructor_dashboard')
        else:
            return redirect('student_dashboard')
    return render(request, 'core/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the home view, which will then redirect to the correct dashboard
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@role_required('student')
def student_dashboard_view(request):
    # This logic will be expanded in Phase 4
    enrolled_courses = Course.objects.filter(enrolled_students__student=request.user)
    all_courses = Course.objects.exclude(id__in=enrolled_courses.values_list('id', flat=True))

    context = {
        'enrolled_courses': enrolled_courses,
        'all_courses': all_courses,
    }
    return render(request, 'core/student_dashboard.html', context)


@login_required
@role_required('instructor')
def instructor_dashboard_view(request):
    # This logic will be expanded in Phase 4
    my_courses = Course.objects.filter(instructor=request.user)
    context = {
        'my_courses': my_courses
    }
    return render(request, 'core/instructor_dashboard.html', context)