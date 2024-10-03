from django.contrib import admin
from .models import BoardingHouse, Booking

class BoardingHouseInline(admin.StackedInline):
    model = BoardingHouse
    readonly_fields = ('boarding_house_id', 'created_at', 'updated_at')
    extra = 0

class BookingInline(admin.TabularInline):
    model = Booking
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    extra = 0

class BoardingHouseAdmin(admin.ModelAdmin):
    list_display = ('boarding_house_id', 'name', 'account_id', 'created_at', 'updated_at', 'available')
    readonly_fields = ('boarding_house_id', 'created_at', 'updated_at')
    inlines = [BookingInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'created_at', 'updated_at', 'booking_status')

# Register your models here.
admin.site.register(BoardingHouse, BoardingHouseAdmin)
admin.site.register(Booking, BookingAdmin)
