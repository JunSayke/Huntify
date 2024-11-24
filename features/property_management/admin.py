from django.contrib import admin

from features.property_management.models import BoardingHouse, BoardingHouseImage, BoardingRoom, BoardingRoomTag, Tag, \
    BoardingRoomImage, Booking

# Register your models here.
admin.site.register(BoardingHouse)
admin.site.register(BoardingHouseImage)
admin.site.register(BoardingRoom)
admin.site.register(BoardingRoomImage)
admin.site.register(BoardingRoomTag)
admin.site.register(Tag)
admin.site.register(Booking)
