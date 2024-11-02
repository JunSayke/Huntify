from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class AccountType(models.TextChoices):
    TENANT = 'tenant'
    LANDLORD = 'landlord'

class CustomUser(AbstractUser):
    id = models.UUIDField(_('user id'), primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='imgs/profile_pictures/', blank=True, null=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    account_type = models.CharField(_('account type'), max_length=10, choices=AccountType.choices, default=AccountType.TENANT)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)