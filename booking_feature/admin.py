from django.contrib import admin
from .models import *

class BoardingHouseImageInline(admin.TabularInline):
    model = BoardingHouseImage
    readonly_fields = ('id', 'uploaded_at')
    extra = 1
    max_num = 5

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    readonly_fields = ('id', 'uploaded_at')
    extra = 1
    max_num = 5

class BoardingHouseInline(admin.StackedInline):
    model = BoardingHouse
    readonly_fields = ('id', 'created_at', 'updated_at')
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    readonly_fields = ('id', 'created_at', 'updated_at')
    extra = 0

class BookingInline(admin.TabularInline):
    model = Booking
    readonly_fields = ('id', 'created_at', 'updated_at')
    extra = 0

class BoardingHouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'account_id', 'created_at', 'updated_at', 'total_rooms', 'available_rooms', 'price_range')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [BoardingHouseImageInline, RoomInline]

    def total_rooms(self, obj):
        return obj.total_rooms

    def available_rooms(self, obj):
        return obj.available_rooms
    
    def price_range(self, obj):
        return obj.price_range

    total_rooms.short_description = 'Total Rooms'
    available_rooms.short_description = 'Available Rooms'
    price_range.short_description = 'Price Range'

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'boarding_house_id', 'created_at', 'updated_at', 'price', 'is_available')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [RoomImageInline, BookingInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'booking_status')

# Register your models here.
admin.site.register(BoardingHouse, BoardingHouseAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BoardingHouseImage)
admin.site.register(RoomImage)

