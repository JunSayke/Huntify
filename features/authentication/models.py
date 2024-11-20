import os

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utilities.mixin import UUIDPKMixin
from utilities.validators import philippine_phone_validator


# Create your models here.
class UserManager(DefaultUserManager):
    def get_queryset(self):
        if hasattr(self.model, 'Type'):
            user_type = getattr(self.model, 'user_type')
            if user_type in self.model.Type:
                return super().get_queryset().filter(user_type=user_type)
        return super().get_queryset()


def user_avatar_image_path(instance, filename):
    return os.path.join('images/profile_picture', str(instance.id), filename)


class User(AbstractUser, UUIDPKMixin):
    class Type(models.TextChoices):
        TENANT = 'tenant', 'Tenant'
        LANDLORD = 'landlord', 'Landlord'
        ADMIN = 'admin', 'Admin'

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    profile_picture = models.ImageField(_('profile picture'), upload_to=user_avatar_image_path, blank=True,
                                        null=True)
    gender = models.CharField(_("gender"), max_length=10, choices=Gender.choices, default=Gender.OTHER)
    phone_number = models.CharField(_('phone number'), max_length=11, validators=[
        philippine_phone_validator
    ], blank=True, null=True, unique=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    street = models.CharField(_('street'), max_length=255, blank=True, null=True)
    province = models.ForeignKey('address.Province', on_delete=models.SET_NULL, blank=True, null=True)
    municipality = models.ForeignKey('address.Municipality', on_delete=models.SET_NULL, blank=True, null=True)
    barangay = models.ForeignKey('address.Barangay', on_delete=models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    user_type = models.CharField(_("user type"), max_length=10, choices=Type.choices, default=Type.TENANT)

    objects = UserManager()

    def address(self):
        return f"{self.street}, {self.barangay}, {self.municipality}, {self.province}".title()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('authentication:profile', kwargs={'pk': self.pk})

    def __str__(self):
        return self.email or self.username


class Tenant(User):
    user_type = User.Type.TENANT

    class Meta:
        proxy = True


class Landlord(User):
    user_type = User.Type.LANDLORD

    class Meta:
        proxy = True


class Admin(User):
    user_type = User.Type.ADMIN

    class Meta:
        proxy = True
