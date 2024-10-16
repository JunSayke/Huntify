from django import forms
from .models import *
from utilities.fields import ValidatedMultiImageField

class BoardingHouseForm(forms.ModelForm):
    images = ValidatedMultiImageField(min_num=0, max_num=5, max_file_size=1024*1024*5)  # 5MB max per file

    class Meta:
        model = BoardingHouse
        fields = ['name', 'description', 'address', 'images']

    def save(self, commit=True):
        instance = super(BoardingHouseForm, self).save(commit)
        for each in self.cleaned_data['images']:
            BoardingHouseImage.objects.create(image=each, boarding_house_id=instance)

        return instance

class RoomForm(forms.ModelForm):
    images = ValidatedMultiImageField(min_num=0, max_num=5, max_file_size=1024*1024*5)  # 5MB max per file

    class Meta:
        model = Room
        fields = ['name', 'description', 'price', 'is_available']

    def save(self, commit=True):
        instance = super(RoomForm, self).save(commit)
        for each in self.cleaned_data['images']:
            RoomImage.objects.create(image=each, room=instance)

        return instance

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
