from django.urls import path
from . import views

app_name = "property_management"

# TODO: Secure Endpoints
urlpatterns = [
    path("dashboard/booking-management/", views.booking_management, name="booking-management"),
    path("dashboard/property-management/", views.BoardingHouseListView.as_view(),
         name="dashboard"),
    path("dashboard/property-management/boarding-houses/", views.BoardingHouseListView.as_view(),
         name="dashboard-boarding-houses"),
    path("dashboard/property-management/delete-boarding-house/<int:boarding_house_id>/",
         views.delete_boarding_house,
         name="delete-boarding-house"),
    path("dashboard/property-management/create-boarding-house/", views.create_boarding_house,
         name="create-boarding-house"),

    path("dashboard/property-management/boarding-rooms/", views.BoardingRoomListView.as_view(),
         name="dashboard-boarding-rooms"),
    path("dashboard/property-management/delete-boarding-room/<int:boarding_room_id>/", views.delete_boarding_room,
         name="delete-boarding-room"),
    path("dashboard/property-management/create-boarding-room/", views.create_boarding_room,
         name="create-boarding-room"),

    path("ajax/get-property/<str:property_type>/", views.get_property, name="get-property"),

    path("rent-a-room/", views.rent_a_room, name="rent-a-room"),
    path("boarding-house-rooms/", views.boarding_house_rooms, name="boarding-house-rooms"),
    path("boarding-house-detail/", views.boarding_house_detail, name="boarding-house-detail"),
    path("boarding-room-detail/", views.boarding_room_detail, name="boarding-room-detail"),
]
