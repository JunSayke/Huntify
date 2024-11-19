from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Tenant, Landlord
from ..address.models import Municipality, Barangay


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


# TODO: Validate birthdate must be before the current date
class AdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birthdate']


class UpdateUserProfileForm(forms.ModelForm):
    prefix = 'update-user_profile_form'

    class Meta:
        model = User
        fields = ['email', 'profile_picture', 'first_name', 'last_name']


class UpdatePhoneNumberForm(forms.ModelForm):
    prefix = 'update-phone_number_form'

    class Meta:
        model = User
        fields = ['phone_number']


class UpdateUserAddressForm(forms.ModelForm):
    prefix = 'update-user_address_form'

    class Meta:
        model = User
        fields = ['province', 'municipality', 'barangay', 'street']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].empty_label = "Select a province"
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['municipality'].empty_label = "Select a municipality"
        self.fields['barangay'].queryset = Barangay.objects.none()
        self.fields['barangay'].empty_label = "Select a barangay"

        province_html_name = self.add_prefix('province')
        municipality_html_name = self.add_prefix('municipality')

        if province_html_name in self.data:
            try:
                province_id = int(self.data.get(province_html_name))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass

        if municipality_html_name in self.data:
            try:
                municipality_id = int(self.data.get(municipality_html_name))
                self.fields['barangay'].queryset = Barangay.objects.filter(municipality_id=municipality_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['municipality'].queryset = self.instance.province.municipality_set.order_by('name')
            self.fields['barangay'].queryset = self.instance.municipality.barangay_set.order_by('name')
