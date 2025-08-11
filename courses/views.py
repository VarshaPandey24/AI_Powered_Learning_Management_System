# courses/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from .forms import CourseForm
from .models import Course, Video, Enrollment
from django.conf import settings
from django.http import HttpResponse


@login_required
@role_required('instructor')
def course_create_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def course_detail_view(request, course_id):
    course = Course.objects.get(pk=course_id)
    # Get all videos for this course, ordered by when they were created
    videos = course.videos.all().order_by('created_at')
    
    context = {
        'course': course,
        'videos': videos, # Add the videos to the context
    }
    return render(request, 'courses/course_detail.html', context)
# courses/views.py

# ... (other imports)
from .models import Course, Video # Make sure Video is imported
from .forms import CourseForm, VideoForm # Import VideoForm
from django.http import HttpResponseForbidden # Import this for the security check

# ... (course_create_view and course_detail_view) ...

@login_required
@role_required('instructor')
def video_add_view(request, course_id):
    course = Course.objects.get(pk=course_id)
    
    # Security check: ensure the user is the instructor of this course
    if course.instructor != request.user:
        return HttpResponseForbidden("You are not allowed to add videos to this course.")

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            # Redirect back to the course detail page
            return redirect('course_detail', course_id=course.id)
    else:
        form = VideoForm()
    
    context = {
        'form': form,
        'course': course
    }
    return render(request, 'courses/video_form.html', context)


@login_required
def course_detail_view(request, course_id):
    course = Course.objects.get(pk=course_id)
    videos = course.videos.all()
    
    # Check if the student is enrolled
    is_enrolled = False
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'student':
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    context = {
        'course': course,
        'videos': videos,
        'is_enrolled': is_enrolled # Add the enrollment status to the context
    }
    return render(request, 'courses/course_detail.html', context)

# courses/views.py

# ... (other imports)
from .models import Course, Enrollment # Make sure Enrollment is imported

# ... (other views) ...

@login_required
def enrollment_confirmation_view(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {
        'course': course
    }
    return render(request, 'courses/enrollment_confirmation.html', context)

@login_required
def process_enrollment_view(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(pk=course_id)
        
        # Prevent duplicate enrollments
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            Enrollment.objects.create(student=request.user, course=course)
        
        return redirect('student_dashboard')
    
    return redirect('home')
