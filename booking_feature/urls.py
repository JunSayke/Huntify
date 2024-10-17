from django.urls import path
from .views import *
from utilities.decorators import ownership_required
from booking_feature.models import BoardingHouse, Room

# Define the lambda function to get the BoardingHouse object
get_boarding_house = lambda request, *args, **kwargs: BoardingHouse.objects.get(id=kwargs['boarding_house_id']) # kwargs['boarding_house_id'] is the value of the keyword argument in the URL pattern

# Define the lambda function to get the BoardingHouse object from the Room object
get_boarding_house_from_room = lambda request, *args, **kwargs: Room.objects.get(id=kwargs['room_id']).boarding_house_id

urlpatterns = [
    path('boarding-house/create/', BoardingHouseCreateView.as_view(), name='add_boarding_house'),
    path('boarding-house/<uuid:boarding_house_id>/edit/', ownership_required(
            get_boarding_house, 
            owner_field='account_id', 
            redirect_url='/', 
            allow_superuser=True
        )(BoardingHouseUpdateView.as_view()), name='edit_boarding_house'),
    path('boarding-house/<uuid:boarding_house_id>/', BoardingHouseDetailView.as_view(), name='boarding_house_detail'),
    path('boarding-house/list', BoardingHouseListView.as_view(), name='boarding_house_list'),
    path('boarding-house/<uuid:boarding_house_id>/delete/', ownership_required(
             get_boarding_house, 
             owner_field='account_id', 
             redirect_url='/',
             allow_superuser=True
         )(BoardingHouseDeleteView.as_view()), name='delete_boarding_house'),

    path('boarding_house/<uuid:boarding_house_id>/room/list', RoomListView.as_view(), name='room_list'),
    path('boarding_house/<uuid:boarding_house_id>/room/add', ownership_required(
             get_boarding_house, 
             owner_field='account_id', 
             redirect_url='/',
             allow_superuser=True
         )(RoomCreateView.as_view()), name='add_room'),
    path('room/<uuid:room_id>/edit', ownership_required(
             get_boarding_house_from_room, 
             owner_field='account_id', 
             redirect_url='/',
             allow_superuser=True
         )(RoomUpdateView.as_view()), name='edit_room'),
    path('room/<uuid:room_id>/', RoomDetailView.as_view(), name='room_detail'),
    path('room/<uuid:room_id>/delete/', ownership_required(
             get_boarding_house_from_room, 
             owner_field='account_id', 
             redirect_url='/',
             allow_superuser=True
         )(RoomDeleteView.as_view()), name='delete_room'),
]