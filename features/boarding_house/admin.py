from django.contrib import admin

from features.boarding_house.models import BoardingHouse, BoardingHouseImage

# Register your models here.
admin.site.register(BoardingHouse)
admin.site.register(BoardingHouseImage)
