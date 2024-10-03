from django.db import models
import uuid

# Create your models here.
class BookingStatus(models.TextChoices):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'

class BoardingHouse(models.Model):
    boarding_house_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey('authentication_feature.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey('authentication_feature.CustomUser', on_delete=models.CASCADE)
    boarding_house_id = models.ForeignKey('BoardingHouse', on_delete=models.CASCADE)
    booking_schedule = models.DateTimeField()
    booking_status = models.CharField(max_length=10, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_id} - {self.bhouse_id}'