from django import forms
from .models import BoardingHouse, Booking

class BoardingHouseForm(forms.ModelForm):
    class Meta:
        model = BoardingHouse
        fields = ['name', 'description', 'address', 'price']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
