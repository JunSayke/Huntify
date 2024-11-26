# forms.py
from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    prefix = 'create-room_rating'

    class Meta:
        model = Rating
        fields = '__all__'
        exclude = ['user', 'boarding_room']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(5, 0, -1)]),  # Reversed order of choices 5 to 1
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40})  # Textarea for feedback
        }
