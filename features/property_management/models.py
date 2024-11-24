# models.py
import os
from random import choice

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from utilities.validators import philippine_phone_validator


def boarding_house_image_path(instance, filename):
    return os.path.join('boarding_house', str(instance.boarding_house.id), 'files', filename)


def boarding_room_image_path(instance, filename):
    return os.path.join('boarding_room', str(instance.boarding_room.id), 'files', filename)


class BoardingHouse(models.Model):
    landlord = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    province = models.ForeignKey('address.Province', on_delete=models.SET_NULL, null=True)
    municipality = models.ForeignKey('address.Municipality', on_delete=models.SET_NULL, null=True)
    barangay = models.ForeignKey('address.Barangay', on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def address(self):
        return f"{self.barangay}, {self.municipality}, {self.province}".title()

    def status(self):
        return self.rooms.filter(is_available=True).count()

    def total_rooms(self):
        return self.rooms.count()

    def random_image(self):
        image = choice(self.images.all()) if self.images.exists() else None
        return image.image.url if image else None

    def first_image(self):
        image = self.images.first() if self.images.exists() else None
        return image.image.url if image else None

    def get_images(self, max_images=5):
        images = list(self.images.all()[:max_images])

        while len(images) < max_images:
            images.append(None)
        return images

    def price_range(self):
        rooms = self.rooms.all()
        if rooms.exists():
            min_price = rooms.order_by('price').first().price
            max_price = rooms.order_by('-price').first().price
            return f"₱{min_price} - ₱{max_price}"
        return None

    def get_existing_images(self):
        return self.images.all()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('property_management:boarding-house', kwargs={'pk': self.pk})


class BoardingHouseImage(models.Model):
    boarding_house = models.ForeignKey(BoardingHouse, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boarding_house_image_path)

    # HACK: Find an optimize way to get the position of the image
    def __str__(self):
        images = list(self.boarding_house.images.select_related('boarding_house').all())
        position = images.index(self) + 1
        return f"{self.boarding_house.name} - Image {position}"


class BoardingRoom(models.Model):
    boarding_house = models.ForeignKey(BoardingHouse, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=2000)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status(self):
        return 'Available' if self.is_available else 'Not Available'

    def full_name(self):
        return f"{self.boarding_house.name} - {self.name}"

    def random_image(self):
        image = choice(self.images.all()) if self.images.exists() else None
        return image.image.url if image else None

    def first_image(self):
        image = self.images.first() if self.images.exists() else None
        return image.image.url if image else None

    def get_images(self, max_images=5):
        images = list(self.images.all()[:max_images])
        while len(images) < max_images:
            images.append(None)  # Append None to represent placeholders
        return images

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('property_management:boarding-room', kwargs={'pk': self.pk})


class BoardingRoomImage(models.Model):
    boarding_room = models.ForeignKey(BoardingRoom, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boarding_room_image_path)

    # HACK: Find an optimize way to get the position of the image
    def __str__(self):
        images = list(self.boarding_room.images.select_related('boarding_room').all())
        position = images.index(self) + 1
        return f"{self.boarding_room.name} - Image {position}"


class BoardingRoomTag(models.Model):
    boarding_room = models.ForeignKey(BoardingRoom, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name


class Tag(models.Model):
    class Type(models.TextChoices):
        BOARDING_ROOM = 'boarding_room', 'Boarding Room'
        BOARDING_HOUSE = 'boarding_house', 'Boarding House'

    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.BOARDING_ROOM)

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    tenant = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    boarding_room = models.ForeignKey(BoardingRoom, on_delete=models.CASCADE)
    visit_time = models.TimeField(null=True, blank=True)
    visit_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20, validators=[philippine_phone_validator])
    message = models.TextField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_processing(self):
        return self.status == 'pending' or self.status == 'approved'

    def __str__(self):
        return f"{self.tenant} - {self.boarding_room} - {self.status}"
