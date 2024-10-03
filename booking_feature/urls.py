from django.urls import path
from .views import BoardingHouseCreateView, BoardingHouseUpdateView, BoardingHouseDetailView

urlpatterns = [
    path('boarding-house/create', BoardingHouseCreateView.as_view(), name='add_boarding_house'),
    path('boarding-house/update/<str:pk>', BoardingHouseUpdateView.as_view(), name='edit_boarding_house'),
    path('boarding-house/<str:pk>', BoardingHouseDetailView.as_view(), name='boarding_house_detail'),
]