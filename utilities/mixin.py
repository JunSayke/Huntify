from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse_lazy, reverse

class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    handle_no_permission_redirect = 'HTTP_REFERER'
    handle_no_permission_default_redirect = reverse_lazy('home')

    def handle_no_permission(self):
        # Redirect to HTTP referrer if available, otherwise redirect to home
        return redirect(self.request.META.get(self.handle_no_permission_redirect, self.handle_no_permission_default_redirect))

class RefererSuccessUrlMixin:
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('home'))

class Handle404RedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect(self.get_404_redirect_url())
        
    def get_404_redirect_url(self):
        return reverse('home')  # Default redirect URL

    