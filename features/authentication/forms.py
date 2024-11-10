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


class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birthdate']


class UpdateUserProfileForm(forms.ModelForm):
    prefix = 'update_user_profile_form'

    class Meta:
        model = User
        fields = ['email', 'profile_picture', 'first_name', 'last_name']


class UpdateUserAddressForm(forms.ModelForm):
    prefix = 'update_user_address_form'

    class Meta:
        model = User
        fields = ['province', 'municipality', 'barangay', 'street']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].required = True
        self.fields['municipality'].required = True
        self.fields['barangay'].required = True
        self.fields['street'].required = True
