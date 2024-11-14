from django.shortcuts import render, redirect
from django.views import View

from features.property_management.forms import CreateBoardingHouseForm, CreateBoardingRoomForm
from features.property_management.models import BoardingHouse, BoardingRoom


# Create your views here.
def booking_management(request):
    return render(request, 'property_management/dashboard/booking-management.html')


def rent_a_room(request):
    return render(request, 'property_management/rent_a_room.html')


def boarding_house_detail(request):
    return render(request, 'property_management/boarding_house_detail.html')


def boarding_room_detail(request):
    return render(request, 'property_management/boarding_room_detail.html')


def boarding_house_rooms(request):
    return render(request, 'property_management/boarding_house_rooms.html')


def get_property(request, property_type=None):
    if property_type == 'boarding_houses':
        boarding_houses = BoardingHouse.objects.filter(landlord=request.user)
        return render(request, 'property_management/dashboard/boarding-house-table.html',
                      {'boarding_houses': boarding_houses})

    boarding_rooms = BoardingRoom.objects.filter(boarding_house__landlord=request.user)
    return render(request, 'property_management/dashboard/boarding-room-table.html',
                  {'boarding_rooms': boarding_rooms})


class PropertyManagementView(View):
    def get(self, request, *args, **kwargs):
        form1 = CreateBoardingHouseForm()
        form2 = CreateBoardingRoomForm(landlord=request.user)

        return render(request, 'property_management/dashboard/property_management.html',
                      {
                          'form1': form1,
                          'form2': form2,
                      })

    def post(self, request, *args, **kwargs):
        form1 = CreateBoardingHouseForm(request.POST, request.FILES)
        form2 = CreateBoardingRoomForm(landlord=request.user, data=request.POST, files=request.FILES)

        if CreateBoardingHouseForm.form_name in request.POST:
            if form1.is_valid():
                form1.instance.landlord = request.user
                form1.save()

                return redirect('property_management:property-management')
        if CreateBoardingRoomForm.form_name in request.POST:
            if form2.is_valid():
                form2.save()

                return redirect('property_management:property-management')

        return render(request, 'property_management/dashboard/property_management.html',
                      {
                          'form1': form1,
                          'form2': form2,
                      })
