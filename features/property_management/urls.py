from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "property_management"

# TODO: Secure Endpoints
urlpatterns = [
    path("dashboard/booking-management/", login_required(views.BookingListView.as_view()), name="booking-management"),
    path("dashboard/booking-management/bookings/", login_required(views.BookingListView.as_view()),
         name="dashboard-bookings"),
    path("dashboard/booking-management/booking/<int:pk>/", login_required(views.BookingDetailView.as_view()), name="booking"),

    path("dashboard/property-management/", login_required(views.BoardingHouseListView.as_view()),
         name="dashboard"),
    path("dashboard/property-management/boarding-houses/", login_required(views.BoardingHouseListView.as_view()),
         name="dashboard-boarding-houses"),
    path("dashboard/property-management/boarding-rooms/", login_required(views.BoardingRoomListView.as_view()),
         name="dashboard-boarding-rooms"),

    path("dashboard/property-management/boarding-houses/create/", login_required(views.BoardingHouseCreateView.as_view()),
         name="create-boarding-house"),
    path("dashboard/property-management/boarding-house/<int:pk>/edit", login_required(views.BoardingHouseUpdateView.as_view()),
         name="update-boarding-house"),

    path("dashboard/property-management/boarding-rooms/create/", login_required(views.BoardingRoomCreateView.as_view()),
         name="create-boarding-room"),
    path("dashboard/property-management/boarding-room/<int:pk>/edit", login_required(views.BoardingRoomUpdateView.as_view()),
         name="update-boarding-room"),

    path("dashboard/tenant-management/", login_required(views.RoomTenantListView.as_view()), name="tenant-management"),
    path("dashboard/tenant-management/<str:tenant_status>/", login_required(views.RoomTenantListView.as_view()),
         name="dashboard-tenants"),

    path("landlords/", views.LandlordListView.as_view(), name="landlords"),
    path("rent-a-room/", views.RentARoomListView.as_view(), name="rent-a-room"),

    path("boarding-room/<int:pk>/", views.BoardingRoomDetailView.as_view(), name="boarding-room"),
    path("boarding-house/<int:pk>/", views.BoardingHouseDetailView.as_view(), name="boarding-house"),
]
