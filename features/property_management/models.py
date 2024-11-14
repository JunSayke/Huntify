# models.py
import os

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


def boarding_house_image_path(instance, filename):
    return os.path.join('boarding_house', str(instance.boarding_house.id), 'files', filename)


def boarding_room_image_path(instance, filename):
    return os.path.join('boarding_room', str(instance.boarding_room.id), 'files', filename)


class BoardingHouse(models.Model):
    landlord = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    boarding_house_name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    province = models.ForeignKey('address.Province', on_delete=models.SET_NULL, null=True)
    municipality = models.ForeignKey('address.Municipality', on_delete=models.SET_NULL, null=True)
    barangay = models.ForeignKey('address.Barangay', on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status(self):
        return self.rooms.filter(is_available=True).count()

    def __str__(self):
        return self.boarding_house_name

    def get_absolute_url(self):
        return reverse('property_management:detail', kwargs={'pk': self.pk})


class BoardingHouseImage(models.Model):
    boarding_house = models.ForeignKey(BoardingHouse, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boarding_house_image_path)

    # HACK: Find an optimize way to get the position of the image
    def __str__(self):
        images = list(self.boarding_house.images.select_related('boarding_house').all())
        position = images.index(self) + 1
        return f"{self.boarding_house.boarding_house_name} - Image {position}"


class BoardingRoom(models.Model):
    boarding_house = models.ForeignKey(BoardingHouse, related_name='rooms', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=2000)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status(self):
        return 'Available' if self.is_available else 'Not Available'

    def __str__(self):
        return self.room_name

    def get_absolute_url(self):
        return reverse('property_management:room_detail', kwargs={'pk': self.pk})


class BoardingRoomImage(models.Model):
    boarding_room = models.ForeignKey(BoardingRoom, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boarding_room_image_path)

    # HACK: Find an optimize way to get the position of the image
    def __str__(self):
        images = list(self.boarding_room.images.select_related('boarding_room').all())
        position = images.index(self) + 1
        return f"{self.boarding_room.room_name} - Image {position}"


class BoardingRoomTag(models.Model):
    boarding_room = models.ForeignKey(BoardingRoom, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag


class Tag(models.Model):
    class Type(models.TextChoices):
        BOARDING_ROOM = 'boarding_room', 'Boarding Room'

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=Type.choices, default=Type.BOARDING_ROOM)

    def __str__(self):
        return self.name
