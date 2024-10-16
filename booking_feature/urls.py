from django.urls import path
from .views import BoardingHouseCreateView, BoardingHouseUpdateView, BoardingHouseDetailView, BoardingHouseListView, RoomCreateView
from utilities.decorators import ownership_required
from booking_feature.models import BoardingHouse

# Define the lambda function to get the BoardingHouse object
get_boarding_house = lambda request, *args, **kwargs: BoardingHouse.objects.get(id=kwargs['boarding_house_id']) # kwargs['boarding_house_id'] is the value of the keyword argument in the URL pattern

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
    path('boarding-house/<uuid:boarding_house_id>/add-room/', ownership_required(
             get_boarding_house, 
             owner_field='account_id', 
             redirect_url='/',
             allow_superuser=True
         )(RoomCreateView.as_view()), name='add_room'),
]