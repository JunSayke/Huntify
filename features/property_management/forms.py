from django import forms
from django.shortcuts import get_object_or_404

from features.address.models import Barangay, Municipality
from .models import BoardingHouse, BoardingRoom, Tag, BoardingHouseImage, BoardingRoomImage, BoardingRoomTag, Booking


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
    prefix = 'create-boarding_house'
    images = MultipleImageField(required=False, max_images=5)

    class Meta:
        model = BoardingHouse
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'landlord']

    def __init__(self, landlord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.landlord = landlord
        self.fields['province'].empty_label = "Choose a province"
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['municipality'].empty_label = "Choose a municipality"
        self.fields['barangay'].queryset = Barangay.objects.none()
        self.fields['barangay'].empty_label = "Choose a barangay"

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

    def save(self, commit=True):
        boarding_house = super().save(commit=False)
        boarding_house.landlord = self.landlord
        if commit:
            boarding_house.save()
            images = self.files.getlist(self.add_prefix('images'))
            for image in images:
                BoardingHouseImage.objects.create(boarding_house=boarding_house, image=image)
        return boarding_house


class UpdateBoardingHouseForm(forms.ModelForm):
    prefix = 'update-boarding_house'
    images = MultipleImageField(required=False, max_images=5)

    class Meta:
        model = BoardingHouse
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'landlord']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].empty_label = "Choose a province"
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['municipality'].empty_label = "Choose a municipality"
        self.fields['barangay'].queryset = Barangay.objects.none()
        self.fields['barangay'].empty_label = "Choose a barangay"

        province_html_name = self.add_prefix('province')
        municipality_html_name = self.add_prefix('municipality')
        images = self.files.getlist(self.add_prefix('images'))
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

    def save(self, commit=True):
        boarding_house = super().save(commit=False)
        if commit:
            boarding_house.save()
            # Delete existing images
            BoardingHouseImage.objects.filter(boarding_house=boarding_house).delete()
            # Save new images
            images = self.files.getlist(self.add_prefix('images'))
            for image in images:
                BoardingHouseImage.objects.create(boarding_house=boarding_house, image=image)
        return boarding_house


class UpdateBoardingRoomForm(forms.ModelForm):
    prefix = 'update-boarding_room'
    images = MultipleImageField(required=False, max_images=5)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type=Tag.Type.BOARDING_ROOM),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BoardingRoom
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.landlord = self.instance.boarding_house.landlord
        self.fields['boarding_house'].queryset = BoardingHouse.objects.filter(landlord=self.landlord)
        self.fields['boarding_house'].empty_label = "Select a boarding house"

        # Set initial values for tags and images
        self.fields['tags'].initial = self.instance.tags.values_list('id', flat=True)
        print()
        self.initial['images'] = [image.image.url for image in self.instance.images.all()]

    def clean_boarding_house(self):
        boarding_house_id = self.cleaned_data.get('boarding_house')
        if not boarding_house_id:
            raise forms.ValidationError("This field is required.")
        boarding_house = get_object_or_404(BoardingHouse, id=boarding_house_id.id, landlord=self.landlord)
        return boarding_house

    def save(self, commit=True):
        boarding_room = super().save(commit=False)
        if commit:
            boarding_room.save()
            # Delete existing images
            BoardingRoomImage.objects.filter(boarding_room=boarding_room).delete()
            # Save new images
            images = self.files.getlist(self.add_prefix('images'))
            for image in images:
                BoardingRoomImage.objects.create(boarding_room=boarding_room, image=image)
            # Delete existing tags
            BoardingRoomTag.objects.filter(boarding_room=boarding_room).delete()
            # Save new tags
            tags = self.cleaned_data.get("tags")
            for tag in tags:
                BoardingRoomTag.objects.create(boarding_room=boarding_room, tag=tag)
        return boarding_room


class CreateBoardingRoomForm(forms.ModelForm):
    prefix = 'create-boarding_room'
    images = MultipleImageField(required=False, max_images=5)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type=Tag.Type.BOARDING_ROOM),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    quantity = forms.IntegerField(min_value=1, max_value=5, initial=1)

    class Meta:
        model = BoardingRoom
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'is_available']

    def __init__(self, landlord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.landlord = landlord
        self.fields['boarding_house'].queryset = BoardingHouse.objects.filter(landlord=landlord)
        self.fields['boarding_house'].empty_label = "Select a boarding house"

    def clean_boarding_house(self):
        boarding_house_id = self.cleaned_data.get('boarding_house')
        if not boarding_house_id:
            raise forms.ValidationError("This field is required.")
        boarding_house = get_object_or_404(BoardingHouse, id=boarding_house_id.id, landlord=self.landlord)
        return boarding_house

    def save(self, commit=True):
        quantity = self.cleaned_data.get('quantity', 1)
        boarding_rooms = []
        for _ in range(quantity):
            boarding_room = super().save(commit=False)
            boarding_room.pk = None  # By setting the primary key to None, a new object will be saved each time.
            if commit:
                boarding_room.save()
                images = self.files.getlist(self.add_prefix('images'))
                for image in images:
                    BoardingRoomImage.objects.create(boarding_room=boarding_room, image=image)
                tags = self.cleaned_data.get('tags')
                for tag in tags:
                    BoardingRoomTag.objects.create(boarding_room=boarding_room, tag=tag)
            boarding_rooms.append(boarding_room)
        return boarding_rooms


class BoardingHouseSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    search_by = forms.ChoiceField(
        choices=[
            ('name', 'Name'),
            ('location', 'Location'),
        ],
        required=False,
        label='Search by'
    )


class BoardingRoomSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    search_by = forms.ChoiceField(
        choices=[
            ('name', 'Name'),
            ('boarding_house', 'Boarding House'),
        ],
        required=False,
        label='Search by'
    )


class RequestBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'contact_number', 'email', 'message',
                  'visit_date', 'visit_time']

    def __init__(self, boarding_room, tenant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boarding_room = boarding_room
        self.tenant = tenant

        if tenant:
            self.fields['first_name'].initial = tenant.first_name
            self.fields['last_name'].initial = tenant.last_name
            self.fields['email'].initial = tenant.email
            self.fields['contact_number'].initial = tenant.phone_number

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.boarding_room = self.boarding_room
        booking.tenant = self.tenant
        if commit:
            booking.save()
        return booking


class BookingSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    search_by = forms.ChoiceField(
        choices=[
            ('tenant', 'Tenant'),
            ('boarding_room', 'Boarding Room'),
            ('boarding_house', 'Boarding House'),
            ('status', 'Status'),
        ],
        required=False,
        label='Search by'
    )


class RoomTenantSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    search_by = forms.ChoiceField(
        choices=[
            ('tenant', 'Tenant'),
            ('boarding_room', 'Boarding Room'),
        ],
        required=False,
        label='Search by'
    )
