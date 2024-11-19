from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from features.property_management.forms import CreateBoardingHouseForm, CreateBoardingRoomForm, BoardingHouseSearchForm, \
    BoardingRoomSearchForm
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
        return render(request, 'property_management/dashboard/boarding_house_table.html',
                      {'boarding_houses': boarding_houses})

    boarding_rooms = BoardingRoom.objects.filter(boarding_house__landlord=request.user)
    return render(request, 'property_management/dashboard/boarding_room_table.html',
                  {'boarding_rooms': boarding_rooms})


# Safe Paginator where it can handle cases where the user tries to access a page that does not exist
class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


class BoardingHouseListView(ListView):
    model = BoardingHouse
    paginator_class = SafePaginator
    context_object_name = 'boarding_houses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_boarding_houses'] = self.get_queryset().count()
        context['search_form'] = BoardingHouseSearchForm(self.request.GET)

        context['create_boarding_house_form'] = CreateBoardingHouseForm(landlord=self.request.user)
        context['create_boarding_room_form'] = CreateBoardingRoomForm(landlord=self.request.user)

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        # current_url = resolve(self.request.path).url_name  # Get URL name

        queryset = queryset.filter(landlord=self.request.user)
        # Handle search query
        query = self.request.GET.get('query', '')
        search_by = self.request.GET.get('search_by', 'name')  # Default to 'name' if not specified
        if query:
            if search_by == 'name':
                queryset = queryset.filter(name__icontains=query)
            elif search_by == 'location':
                queryset = queryset.annotate(
                    location=Concat(
                        'barangay__name', Value(', '),
                        'municipality__name', Value(', '),
                        'province__name'
                    )
                ).filter(location__icontains=query)

        # Handle sorting with direction (ascending or descending)
        sort_by = self.request.GET.get('sort', '')
        direction = self.request.GET.get('direction', 'asc')  # Default direction is ascending
        if sort_by:
            if sort_by == 'name':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}name")
            elif sort_by == 'available_rooms':
                queryset = queryset.annotate(
                    available_rooms=Count('rooms', filter=Q(rooms__is_available=True))
                ).order_by(f"{'-' if direction == 'desc' else ''}available_rooms")
            elif sort_by == 'created_at':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}created_at")

        return queryset

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # Handle creation of a boarding house
        if 'create-boarding_house' in request.POST:
            create_boarding_house_form = CreateBoardingHouseForm(data=request.POST, files=request.FILES,
                                                                 landlord=request.user)
            if create_boarding_house_form.is_valid():
                create_boarding_house_form.save()
                messages.success(request, "Boarding house created successfully.")
            else:
                context['create_boarding_house_form'] = create_boarding_house_form


        # Handle creation of a boarding room
        elif 'create-boarding_room' in request.POST:
            create_boarding_room_form = CreateBoardingRoomForm(data=request.POST, files=request.FILES,
                                                               landlord=request.user)
            if create_boarding_room_form.is_valid():
                create_boarding_room_form.save()
                messages.success(request, "Boarding room created successfully.")
            else:
                context['create_boarding_room_form'] = create_boarding_room_form


        # Handle deletion of a boarding house
        elif 'delete-boarding_house' in request.POST:
            pass
        # Handle deletion of a boarding room
        elif 'delete-boarding_room' in request.POST:
            pass

        return self.render_to_response(context)

    def get_template_names(self):
        # current_url = resolve(self.request.path).url_name
        return ['property_management/dashboard/boarding_house_list.html']


class BoardingRoomListView(ListView):
    model = BoardingRoom
    paginator_class = SafePaginator
    context_object_name = 'boarding_rooms'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # current_url = resolve(self.request.path).url_name  # Get URL name

        form_data = self.request.session.pop('form_data', None)
        form_error = self.request.session.pop('form_error', None)

        context['total_boarding_rooms'] = self.get_queryset().count()
        context['search_form'] = BoardingRoomSearchForm(self.request.GET)
        # OPTIMIZE: Duplicate code as BoardingHouseListView get_context_data
        create_boarding_house_form = CreateBoardingHouseForm(landlord=self.request.user)
        create_boarding_room_form = CreateBoardingRoomForm(landlord=self.request.user)

        if form_data:
            if form_error == "create_boarding_house_form":
                create_boarding_house_form = CreateBoardingHouseForm(form_data, landlord=self.request.user)
            elif form_error == "create_boarding_room_form":
                create_boarding_room_form = CreateBoardingHouseForm(form_data, landlord=self.request.user)

        context['create_boarding_house_form'] = create_boarding_house_form
        context['create_boarding_room_form'] = create_boarding_room_form

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        # current_url = resolve(self.request.path).url_name  # Get URL name

        queryset = queryset.filter(boarding_house__landlord=self.request.user)
        # Handle search query
        query = self.request.GET.get('query', '')
        search_by = self.request.GET.get('search_by', 'name')  # Default to 'name' if not specified
        if query:
            if search_by == 'name':
                queryset = queryset.filter(name__icontains=query)
            elif search_by == 'boarding_house':
                queryset = queryset.filter(boarding_house__name__icontains=query)

        # Handle sorting with direction (ascending or descending)
        sort_by = self.request.GET.get('sort', '')
        direction = self.request.GET.get('direction', 'asc')  # Default direction is ascending
        if sort_by:
            if sort_by == 'name':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}name")
            elif sort_by == 'status':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}is_available")
            elif sort_by == 'boarding_house':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}boarding_house__name")
            elif sort_by == 'created_at':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}created_at")
            elif sort_by == 'price':
                queryset = queryset.order_by(f"{'-' if direction == 'desc' else ''}price")

        return queryset

    def get_template_names(self):
        # current_url = resolve(self.request.path).url_name
        return ['property_management/dashboard/boarding_room_list.html']


@require_http_methods(["POST"])
def delete_boarding_house(request, boarding_house_id):
    if request.method == "POST":
        boarding_house = get_object_or_404(BoardingHouse, id=boarding_house_id)

        # Ensure only authorized users can delete
        if boarding_house.landlord != request.user:
            return HttpResponseForbidden("You are not allowed to delete this item.")

        # Delete the boarding house
        boarding_house.delete()

        # Redirect to referer or fallback
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer or 'authentication:home')


@require_http_methods(["POST"])
def create_boarding_house(request):
    if request.method == 'POST':
        form = CreateBoardingHouseForm(landlord=request.user, data=request.POST, files=request.FILES)
        referer = request.META.get('HTTP_REFERER')

        if form.is_valid():
            form.save()
        else:
            request.session['form_data'] = request.POST
            request.session['form_error'] = "create_boarding_house_form"

        return redirect(referer or 'authentication:home')


@require_http_methods(["POST"])
def delete_boarding_room(request, boarding_room_id):
    if request.method == "POST":
        boarding_room = get_object_or_404(BoardingRoom, id=boarding_room_id)

        # Ensure only authorized users can delete
        if boarding_room.boarding_house.landlord != request.user:
            return HttpResponseForbidden("You are not allowed to delete this item.")

        # Delete the boarding room
        boarding_room.delete()

        # Redirect to referer or fallback
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer or 'authentication:home')


@require_http_methods(["POST"])
def create_boarding_room(request):
    if request.method == 'POST':
        form = CreateBoardingRoomForm(landlord=request.user, data=request.POST, files=request.FILES)
        referer = request.META.get('HTTP_REFERER')

        if form.is_valid():
            form.save()
        else:
            request.session['form_data'] = request.POST
            request.session['form_error'] = "create_boarding_room_form"

        return redirect(referer or 'authentication:home')
