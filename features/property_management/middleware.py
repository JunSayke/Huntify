from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.conf import settings

class DashboardRestrictionMiddleware:
    """
    Middleware to restrict access based on user type.
    Allows access only for users with user_type 'landlord' or 'admin'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Check conditions
        if request.path.startswith('/dashboard/' ):                
            if not user.is_authenticated or not hasattr(user, 'user_type') or user.user_type not in ['landlord', 'admin'] or not user.is_superuser or not user.is_staff:
                return redirect(settings.LOGIN_URL)

        # Allow normal request processing
        return self.get_response(request)
