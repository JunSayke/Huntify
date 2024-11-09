# models.py
from django.db import models
import os


def boarding_house_image_path(instance, filename):
    return os.path.join('boarding_house', str(instance.boarding_house.id), 'files', filename)


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
        return "Active"

    def __str__(self):
        return self.boarding_house_name


class BoardingHouseImage(models.Model):
    boarding_house = models.ForeignKey(BoardingHouse, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boarding_house_image_path)

    def __str__(self):
        images = list(self.boarding_house.images.select_related('boarding_house').all())
        position = images.index(self) + 1
        return f"{self.boarding_house.boarding_house_name} - Image {position}"
