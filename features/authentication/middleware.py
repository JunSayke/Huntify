from django.shortcuts import redirect
from django.urls import reverse


class EnsureProfileCompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/__reload__/'):  # avoid spamming from tailwind auto reload
            return self.get_response(request)

        if request.user.is_authenticated and not request.user.is_superuser:
            sign_out_path = reverse('authentication:logout')
            if request.path != sign_out_path and (
                    not request.user.first_name or not request.user.last_name or not request.user.gender or not request.user.birthdate):
                if request.path != reverse('authentication:personal-information'):
                    return redirect('authentication:personal-information')
        response = self.get_response(request)
        return response
