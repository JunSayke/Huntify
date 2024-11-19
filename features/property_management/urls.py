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
    path("dashboard/property-management/boarding-rooms/", views.BoardingRoomListView.as_view(),
         name="dashboard-boarding-rooms"),

    path("rent-a-room/", views.RentARoomListView.as_view(), name="rent-a-room"),
    path("boarding-room/<int:pk>/", views.BoardingRoomDetailView.as_view(), name="boarding-room"),
    path("boarding-house/<int:pk>/", views.BoardingHouseDetailView.as_view(), name="boarding-house"),
]
