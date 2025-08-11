# core/decorators.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not hasattr(request.user, 'profile') or request.user.profile.role != role:
                # You can redirect to a 'permission denied' page or just the homepage
                return redirect('home') 
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator