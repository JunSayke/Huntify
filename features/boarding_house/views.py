from django.shortcuts import render, redirect
from django.views import View

from features.boarding_house.forms import CreateBoardingHouseForm
from features.boarding_house.models import BoardingHouseImage, BoardingHouse


# Create your views here.
def booking_management(request):
    return render(request, 'boarding_house/dashboard/booking-management.html')


def rent_a_room(request):
    return render(request, 'boarding_house/rent_a_room.html')


def boarding_house_detail(request):
    return render(request, 'boarding_house/boarding_house_detail.html')


def boarding_room_detail(request):
    return render(request, 'boarding_house/boarding_room_detail.html')


def boarding_house_rooms(request):
    return render(request, 'boarding_house/boarding_house_rooms.html')


class PropertyManagementView(View):
    def get(self, request, property_type=None, *args, **kwargs):
        boarding_house_create_form = CreateBoardingHouseForm()

        # OPTIMIZE: Duplicate code
        boarding_houses = BoardingHouse.objects.filter(landlord=request.user)

        if property_type == 'boarding-houses':
            return render(request, 'boarding_house/dashboard/landlord_boarding_houses.html',
                          {
                              'property_type': property_type,
                              'boarding_houses': boarding_houses,
                              'form1': boarding_house_create_form
                          })
        return render(request, 'boarding_house/dashboard/landlord_boarding_rooms.html',
                      {
                          'property_type': property_type,
                          'boarding_houses': boarding_houses,
                          'form1': boarding_house_create_form
                      })

    def post(self, request, property_type=None, *args, **kwargs):
        if 'form1' in request.POST:
            form1 = CreateBoardingHouseForm(request.POST, request.FILES)
            if form1.is_valid():
                boarding_house = form1.save(commit=False)
                boarding_house.landlord = request.user
                boarding_house.save()
                images = request.FILES.getlist('images')
                for image in images:
                    BoardingHouseImage.objects.create(boarding_house=boarding_house, image=image)

                return redirect('boarding_house:property-management', property_type=property_type)
        else:
            form1 = CreateBoardingHouseForm()

        # OPTIMIZE: Duplicate code
        boarding_houses = BoardingHouse.objects.filter(landlord=request.user)

        if property_type == 'boarding-houses':
            return render(request, 'boarding_house/dashboard/landlord_boarding_houses.html',
                          {
                              'property_type': property_type,
                              'boarding_houses': boarding_houses,
                              'form1': form1
                          })
        return render(request, 'boarding_house/dashboard/landlord_boarding_rooms.html',
                      {
                          'property_type': property_type,
                          'boarding_houses': boarding_houses,
                          'form1': form1
                      })
