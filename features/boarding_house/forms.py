# forms.py
from django import forms
from .models import BoardingHouse, BoardingHouseImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, max_images=5, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        self.max_images = max_images
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > self.max_images:
                raise forms.ValidationError(f"You can upload a maximum of {self.max_images} images.")
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateBoardingHouseForm(forms.ModelForm):
    prefix = 'create_boarding_house_form'
    images = MultipleImageField(required=False, max_images=5)

    class Meta:
        model = BoardingHouse
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'landlord']
