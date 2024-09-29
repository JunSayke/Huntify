from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, AccountType

class AccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(choices=AccountType.choices, widget=forms.RadioSelect)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birthdate', 'profile_picture', 'account_type']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields read-only
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        # Add more fields as needed

