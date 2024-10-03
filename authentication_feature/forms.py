from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, AccountType

class AccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(choices=AccountType.choices, widget=forms.RadioSelect,  error_messages={
            'required': 'Please select an account type.'
        })
        

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        
class CustomUserChangeForm(UserChangeForm):
    password = None # Does not include password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'birthdate', 'profile_picture', 'account_type']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }
        exclude = ['account_type']

