from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from features.property_management.forms import CreateBoardingHouseForm, CreateBoardingRoomForm, BoardingHouseSearchForm, \
    BoardingRoomSearchForm, RequestBookingForm
from features.property_management.models import BoardingHouse, BoardingRoom, Tag


# Create your views here.
def booking_management(request):
    return render(request, 'property_management/dashboard/booking-management.html')


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


# TODO: Restrict access to these views to landlords only
# OPTIMIZE: BoardingHouseListView and BoardingRoomListView can be refactored possibly through mixins or inheritance
class BoardingHouseListView(ListView):
    model = BoardingHouse
    paginator_class = SafePaginator
    context_object_name = 'boarding_houses'
    paginate_by = 10
    template_name = 'property_management/dashboard/boarding_house_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_boarding_houses'] = self.get_queryset().count()
        context['search_form'] = BoardingHouseSearchForm(self.request.GET)

        context['create_boarding_house_form'] = CreateBoardingHouseForm(landlord=self.request.user)
        context['create_boarding_room_form'] = CreateBoardingRoomForm(landlord=self.request.user)

        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')

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
                return redirect('property_management:dashboard-boarding-houses')
            else:
                context['create_boarding_house_form'] = create_boarding_house_form


        # Handle creation of a boarding room
        elif 'create-boarding_room' in request.POST:
            create_boarding_room_form = CreateBoardingRoomForm(data=request.POST, files=request.FILES,
                                                               landlord=request.user)
            if create_boarding_room_form.is_valid():
                create_boarding_room_form.save()
                messages.success(request, "Boarding room created successfully.")
                return redirect('property_management:dashboard-boarding-houses')
            else:
                context['create_boarding_room_form'] = create_boarding_room_form


        # Handle deletion of a boarding house
        elif 'delete-boarding_house' in request.POST:
            boarding_house_id = request.POST.get('delete-boarding_house')
            boarding_house = get_object_or_404(BoardingHouse, id=boarding_house_id)

            # Ensure only authorized users can delete
            if boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to delete this item.")

            # Delete the boarding house
            boarding_house.delete()

        return self.render_to_response(context)


class BoardingRoomListView(ListView):
    model = BoardingRoom
    paginator_class = SafePaginator
    context_object_name = 'boarding_rooms'
    paginate_by = 10
    template_name = 'property_management/dashboard/boarding_room_list.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_boarding_rooms'] = self.get_queryset().count()
        context['search_form'] = BoardingRoomSearchForm(self.request.GET)

        context['create_boarding_house_form'] = CreateBoardingHouseForm(landlord=self.request.user)
        context['create_boarding_room_form'] = CreateBoardingRoomForm(landlord=self.request.user)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
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
                return redirect('property_management:dashboard-boarding-houses')
            else:
                context['create_boarding_house_form'] = create_boarding_house_form


        # Handle creation of a boarding room
        elif 'create-boarding_room' in request.POST:
            create_boarding_room_form = CreateBoardingRoomForm(data=request.POST, files=request.FILES,
                                                               landlord=request.user)
            if create_boarding_room_form.is_valid():
                create_boarding_room_form.save()
                messages.success(request, "Boarding room created successfully.")
                return redirect('property_management:dashboard-boarding-houses')
            else:
                context['create_boarding_room_form'] = create_boarding_room_form


        # Handle deletion of a boarding house
        elif 'delete-boarding_room' in request.POST:
            boarding_room_id = request.POST.get('delete-boarding_room')
            boarding_room = get_object_or_404(BoardingRoom, id=boarding_room_id)

            # Ensure only authorized users can delete
            if boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to delete this item.")

            # Delete the boarding room
            boarding_room.delete()

        return self.render_to_response(context)


class RentARoomListView(ListView):
    model = BoardingRoom
    paginator_class = SafePaginator
    context_object_name = 'boarding_rooms'
    paginate_by = 10
    template_name = 'property_management/rent_a_room.html'
    ordering = ['-created_at', '-is_available']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = super().get_queryset()
        context['total_boarding_rooms'] = queryset.count()
        context['tags'] = Tag.objects.filter(type=Tag.Type.BOARDING_ROOM)
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(is_available=True)
        # Handle search query
        address = self.request.GET.get('address', '')
        if address:
            queryset = queryset.annotate(
                location=Concat(
                    'boarding_house__barangay__name', Value(', '),
                    'boarding_house__municipality__name', Value(', '),
                    'boarding_house__province__name'
                )
            ).filter(location__icontains=address)

        # Handle tag filtering
        tags = self.request.GET.getlist('tags')  # Expecting a list of tag IDs from the query parameters
        if tags:
            queryset = queryset.filter(tags__tag__id__in=tags).distinct()

        # Handle price filtering
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset


class BoardingRoomDetailView(DetailView):
    model = BoardingRoom
    template_name = 'property_management/boarding_room_detail.html'
    context_object_name = 'boarding_room'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['landlord'] = self.object.boarding_house.landlord
        context['boarding_house'] = self.object.boarding_house

        tenant = self.request.user
        initial_data = {
            'first_name': tenant.first_name,
            'last_name': tenant.last_name,
            'email': tenant.email,
            'contact_number': tenant.phone_number,
        }

        context['request_booking_form'] = RequestBookingForm(initial=initial_data)
        return context

    # TODO: Restrict access to this method to tenants only
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure self.object is set
        context = self.get_context_data()
        request_booking_form = RequestBookingForm(data=request.POST)
        if request_booking_form.is_valid():
            booking = request_booking_form.save(commit=False)
            booking.boarding_room = self.object
            booking.save()
            messages.success(request, "Booking request sent successfully.")
            return redirect('property_management:boarding-room', pk=self.object.pk)
        else:
            context['request_booking_form'] = request_booking_form
            return self.render_to_response(context)




class BoardingHouseDetailView(DetailView):
    model = BoardingHouse
    template_name = 'property_management/boarding_house_detail.html'
    context_object_name = 'boarding_house'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['landlord'] = self.object.landlord
        context['boarding_rooms'] = self.object.rooms.all()
        return context
