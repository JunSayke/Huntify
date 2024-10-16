from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
class BookingStatus(models.TextChoices):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'

class BoardingHouse(models.Model):
    id = models.UUIDField(_('boarding house id'), primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey('authentication_feature.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(_('boarding house name'), max_length=100)
    description = models.TextField(_('description'))
    address = models.CharField(_('address'), max_length=100)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    @property
    def total_rooms(self):
        return self.rooms.count()

    @property
    def available_rooms(self):
        return self.rooms.filter(is_available=True).count()

    @property
    def price_range(self):
        if prices := self.rooms.values_list('price', flat=True):
            return f"{min(prices)} - {max(prices)}"
        return "No rooms available"

    def __str__(self):
        return self.name
    
class Room(models.Model):
    id = models.UUIDField(_('room id'), primary_key=True, default=uuid.uuid4, editable=False)
    boarding_house_id = models.ForeignKey('BoardingHouse', on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(_('room name'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_available = models.BooleanField(_('is available'), default=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.name
    
class BoardingHouseImage(models.Model):
    id = models.UUIDField(_('image id'), primary_key=True, default=uuid.uuid4, editable=False)
    boarding_house_id = models.ForeignKey(BoardingHouse, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='boarding_house_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RoomImage(models.Model):
    id = models.UUIDField(_('image id'), primary_key=True, default=uuid.uuid4, editable=False)
    room_id = models.ForeignKey('Room', related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='room_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    id = models.UUIDField(_('booking id'), primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey('authentication_feature.CustomUser', on_delete=models.CASCADE)
    room_id = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='bookings')
    booking_schedule = models.DateTimeField(_('schedule'))
    booking_status = models.CharField(_('status'), max_length=10, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f'{self.account_id} - {self.bhouse_id}'
