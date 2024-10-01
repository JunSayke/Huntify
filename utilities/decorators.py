from django.shortcuts import redirect
from django.conf import settings
from functools import wraps

def anonymous_required(function=None, redirect_url=settings.HOME_URL):
    """
    Decorator for views that allow only unauthenticated users to access view.
    """
    def decorator(function):
        @wraps(function)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return function(request, *args, **kwargs)
        return _wrapped_view

    return decorator(function) if function else decorator
