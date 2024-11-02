from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.mixin import UUIDPKMixin


# Create your models here.
class UserManager(DefaultUserManager):
    def get_queryset(self):
        if hasattr(self.model, 'Type'):
            user_type = getattr(self.model, 'user_type')
            if user_type in self.model.Type:
                return super().get_queryset().filter(user_type=user_type)
        return super().get_queryset()


class User(AbstractUser, UUIDPKMixin):
    class Type(models.TextChoices):
        TENANT = 'tenant', 'Tenant'
        LANDLORD = 'landlord', 'Landlord'
        ADMIN = 'admin', 'Admin'

    phone_number = models.EmailField(_('phone number'), blank=True, null=True, unique=True)
    age = models.PositiveIntegerField(_('age'), blank=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    user_type = models.CharField(_("user type"), max_length=10, choices=Type.choices, default=Type.TENANT)

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

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
