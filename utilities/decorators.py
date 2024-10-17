from django.shortcuts import redirect
from django.conf import settings
from functools import wraps
from django.core.exceptions import PermissionDenied

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

def ownership_required(get_object_func, owner_field, redirect_url=None, allow_staff=False, allow_superuser=False):
    """
    Decorator for views that checks that the user is the owner of the object,
    or is a superuser or staff member based on the parameters.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            current_user = request.user
            # Get the object using the provided function
            obj = get_object_func(request, *args, **kwargs)
            # Get the object's owner
            object_owner = getattr(obj, owner_field)

            # Check if the current user is the owner, superuser, or staff
            if current_user != object_owner and not (allow_superuser and current_user.is_superuser) and not (allow_staff and current_user.is_staff):
                # Redirect to the HTTP_REFERER if provided, otherwise raise PermissionDenied
                if redirect_url:
                    return redirect(request.META.get('HTTP_REFERER', redirect_url))
                else:
                    raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator