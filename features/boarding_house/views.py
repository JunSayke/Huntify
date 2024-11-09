from django.shortcuts import render, redirect
from django.views import View

from features.boarding_house.forms import BoardingHouseCreateForm
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
        boarding_house_create_form = BoardingHouseCreateForm()

        # TODO: Optimize duplicate code from post method
        boarding_houses = BoardingHouse.objects.filter(landlord=request.user)

        if property_type == 'boarding-houses':
            return render(request, 'boarding_house/dashboard/landlord_boarding_houses.html',
                          {
                              'property_type': property_type,
                              'boarding_houses': boarding_houses,
                              BoardingHouseCreateForm.form_name: boarding_house_create_form
                          })
        return render(request, 'boarding_house/dashboard/landlord_boarding_rooms.html',
                      {
                          'property_type': property_type,
                          'boarding_houses': boarding_houses,
                          BoardingHouseCreateForm.form_name: boarding_house_create_form
                      })

    def post(self, request, property_type=None, *args, **kwargs):
        if BoardingHouseCreateForm.form_name in request.POST:
            boarding_house_create_form = BoardingHouseCreateForm(request.POST, request.FILES)
            if boarding_house_create_form.is_valid():
                boarding_house = boarding_house_create_form.save(commit=False)
                boarding_house.landlord = request.user
                boarding_house.save()
                images = request.FILES.getlist('images')
                for image in images:
                    BoardingHouseImage.objects.create(boarding_house=boarding_house, image=image)

                return redirect('boarding_house:property-management', property_type=property_type)
            print(boarding_house_create_form.errors)
        else:
            boarding_house_create_form = BoardingHouseCreateForm()

        # TODO: Optimize duplicate code from get method
        boarding_houses = BoardingHouse.objects.filter(landlord=request.user)

        if property_type == 'boarding-houses':
            return render(request, 'boarding_house/dashboard/landlord_boarding_houses.html',
                          {
                              'property_type': property_type,
                              'boarding_houses': boarding_houses,
                              BoardingHouseCreateForm.form_name: boarding_house_create_form
                          })
        return render(request, 'boarding_house/dashboard/landlord_boarding_rooms.html',
                      {
                          'property_type': property_type,
                          'boarding_houses': boarding_houses,
                          BoardingHouseCreateForm.form_name: boarding_house_create_form

                      })
