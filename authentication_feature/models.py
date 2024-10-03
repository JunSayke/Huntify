from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AccountType(models.TextChoices):
    TENANT = 'tenant'
    LANDLORD = 'landlord'

class CustomUser(AbstractUser):
    phone_number = models.EmailField(_('phone number'), blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.TENANT)