from django.urls import path
from . import views

app_name = "boarding_house"

# TODO: Secure Endpoints
urlpatterns = [
    path("dashboard/booking-management/", views.booking_management, name="booking-management"),
    path("dashboard/property-management/", views.PropertyManagementView.as_view(), name="dashboard"),
    path("dashboard/property-management/<str:property_type>/", views.PropertyManagementView.as_view(),
         name="property-management"),

    path("rent-a-room/", views.rent_a_room, name="rent-a-room"),
    path("boarding-house-rooms/", views.boarding_house_rooms, name="boarding-house-rooms"),
    path("boarding-house-detail/", views.boarding_house_detail, name="boarding-house-detail"),
    path("boarding-room-detail/", views.boarding_room_detail, name="boarding-room-detail"),
]
