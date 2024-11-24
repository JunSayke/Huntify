from django.urls import path

from . import views

app_name = "property_management"

# TODO: Secure Endpoints
urlpatterns = [
    path("dashboard/booking-management/", views.BookingListView.as_view(), name="booking-management"),
    path("dashboard/booking-management/bookings/", views.BookingListView.as_view(),
         name="dashboard-bookings"),
    path("dashboard/booking-management/booking/<int:pk>/", views.BookingDetailView.as_view(), name="booking"),

    path("dashboard/property-management/", views.BoardingHouseListView.as_view(),
         name="dashboard"),
    path("dashboard/property-management/boarding-houses/", views.BoardingHouseListView.as_view(),
         name="dashboard-boarding-houses"),
    path("dashboard/property-management/boarding-rooms/", views.BoardingRoomListView.as_view(),
         name="dashboard-boarding-rooms"),

    path("dashboard/property-management/boarding-houses/create/", views.BoardingHouseCreateView.as_view(),
         name="create-boarding-house"),
    path("dashboard/property-management/boarding-house/<int:pk>/edit", views.BoardingHouseUpdateView.as_view(),
         name="update-boarding-house"),

    path("dashboard/property-management/boarding-rooms/create/", views.BoardingRoomCreateView.as_view(),
         name="create-boarding-room"),
    path("dashboard/property-management/boarding-room/<int:pk>/edit", views.BoardingRoomUpdateView.as_view(),
         name="update-boarding-room"),

    path("dashboard/tenant-management/", views.RoomTenantListView.as_view(), name="tenant-management"),
    path("dashboard/tenant-management/tenant/", views.RoomTenantListView.as_view(), name="dashboard-tenants"),

    path("rent-a-room/", views.RentARoomListView.as_view(), name="rent-a-room"),

    path("boarding-room/<int:pk>/", views.BoardingRoomDetailView.as_view(), name="boarding-room"),
    path("boarding-house/<int:pk>/", views.BoardingHouseDetailView.as_view(), name="boarding-house"),
]
