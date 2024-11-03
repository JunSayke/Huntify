from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from .forms import UserTypeForm, TenantRegistrationForm, LandlordRegistrationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView


# Create your views here.
def home(request):
    return render(request, "authentication/home.html")


def profile(request):
    return render(request, "authentication/profile.html")


def change_password(request):
    return render(request, "authentication/change-password.html")


def edit_profile(request):
    return render(request, "authentication/edit-profile.html")


class LogoutView(DjangoLogoutView):
    template_name = "authentication/logout.html"


class LoginView(DjangoLoginView):
    template_name = "authentication/login.html"


class RegistrationWizard(SessionWizardView):
    TEMPLATES = {
        "user_type": "authentication/user_type_form.html",
        "tenant_registration": "authentication/tenant_registration_form.html",
        "landlord_registration": "authentication/landlord_registration_form.html",
    }

    form_list = [
        ("user_type", UserTypeForm),
        ("tenant_registration", TenantRegistrationForm),
        ("landlord_registration", LandlordRegistrationForm),
    ]

    condition_dict = {
        "tenant_registration": lambda self: self.is_tenant(),
        "landlord_registration": lambda self: self.is_landlord(),
    }

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def is_tenant(self):
        user_type = self.get_cleaned_data_for_step('user_type')
        return user_type and user_type.get('user_type') == 'tenant'

    def is_landlord(self):
        user_type = self.get_cleaned_data_for_step('user_type')
        return user_type and user_type.get('user_type') == 'landlord'

    def done(self, form_list, **kwargs):
        for form in form_list:
            if hasattr(form, 'save') and form.cleaned_data:
                form.save()

        # return render(self.request, 'authentication/registration_done.html', {
        #     'form_data': [form.cleaned_data for form in form_list if form.cleaned_data],
        # })
        return redirect('authentication:login')
