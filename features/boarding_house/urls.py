from django.urls import path
from . import views

app_name = "boarding_house"
urlpatterns = [
    path("dashboard/property-management/", views.property_management, name="property-management"),
    path("dashboard/booking-management/", views.booking_management, name="booking-management"),
    path("rent-a-room", views.rent_a_room, name="rent-a-room"),
    path("boarding-house-detail", views.boarding_house_detail, name="boarding-house-detail"),
    path("boarding-room-detail", views.boarding_room_detail, name="boarding-room-detail"),
    path("get-property-table/<str:property_type>", views.get_property_table, name="get-property-table"),
]
