from functools import wraps
from django.shortcuts import render

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return render(request, 'unauthorized.html', {
                    'message': 'You must be logged in as a buyer to access this page.'
                })

            if request.user.role not in allowed_roles:
                return render(request, 'unauthorized.html', {
                    'message': 'Access denied. Only buyers are allowed to rent devices.'
                })

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
