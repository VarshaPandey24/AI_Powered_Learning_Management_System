# courses/urls.py
from django.urls import path
from .views import course_create_view, course_detail_view,video_add_view ,enrollment_confirmation_view,process_enrollment_view 

urlpatterns = [
    path('create/', course_create_view, name='course_create'),
    path('<int:course_id>/', course_detail_view, name='course_detail'), 
    path('<int:course_id>/add-video/', video_add_view, name='video_add'), 
 path('<int:course_id>/enroll/', enrollment_confirmation_view, name='enrollment_confirmation'),
    path('<int:course_id>/process-enrollment/', process_enrollment_view, name='process_enrollment'),
]