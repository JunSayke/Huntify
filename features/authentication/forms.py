from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tenant, Landlord


class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(choices=User.Type.choices, widget=forms.RadioSelect, error_messages={
        'required': 'Please select an account type.'
    })  # Find a cleaner way to remove admin from the choices


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TenantRegistrationForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = Tenant

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.Type.TENANT
        if commit:
            user.save()
        return user


class LandlordRegistrationForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = Landlord

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.Type.LANDLORD
        if commit:
            user.save()
        return user
