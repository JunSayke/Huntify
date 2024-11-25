from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.db import transaction
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from features.authentication.models import User
from features.property_management.forms import CreateBoardingHouseForm, CreateBoardingRoomForm, BoardingHouseSearchForm, \
    BoardingRoomSearchForm, RequestBookingForm, BookingSearchForm, UpdateBoardingHouseForm, UpdateBoardingRoomForm, \
    RoomTenantSearchForm
from features.property_management.models import BoardingHouse, BoardingRoom, Tag, Booking, BoardingRoomTenant
from features.rating.forms import RatingForm


# Create your views here.
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
    template_name = 'property_management/dashboard/property/boarding_house/boarding_house_list.html'

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

        # Handle deletion of a boarding house
        if 'delete-boarding_house' in request.POST:
            boarding_house_id = request.POST.get('delete-boarding_house')
            boarding_house = get_object_or_404(BoardingHouse, id=boarding_house_id)

            # Ensure only authorized users can delete
            if boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to delete this item.")

            messages.success(request, "Boarding house deleted successfully.")
            # Delete the boarding house
            boarding_house.delete()

        return self.render_to_response(context)


class BoardingRoomListView(ListView):
    model = BoardingRoom
    paginator_class = SafePaginator
    context_object_name = 'boarding_rooms'
    paginate_by = 10
    template_name = 'property_management/dashboard/property/boarding_room/boarding_room_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_boarding_rooms'] = self.get_queryset().count()
        context['search_form'] = BoardingRoomSearchForm(self.request.GET)

        context['create_boarding_house_form'] = CreateBoardingHouseForm(landlord=self.request.user)
        context['create_boarding_room_form'] = CreateBoardingRoomForm(landlord=self.request.user)
        context['update_boarding_house_form'] = CreateBoardingHouseForm(landlord=self.request.user)

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

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # Handle deletion of a boarding house
        if 'delete-boarding_room' in request.POST:
            boarding_room_id = request.POST.get('delete-boarding_room')
            boarding_room = get_object_or_404(BoardingRoom, id=boarding_room_id)

            # Ensure only authorized users can delete
            if boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to delete this item.")

            messages.success(request, "Boarding room deleted successfully.")
            # Delete the boarding room
            boarding_room.delete()

        return self.render_to_response(context)


class BoardingHouseCreateView(CreateView):
    model = BoardingHouse
    form_class = CreateBoardingHouseForm
    template_name = 'property_management/dashboard/property/boarding_house/add_boarding_house.html'
    success_url = reverse_lazy('property_management:create-boarding-house')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Boarding house created successfully.")
        return super().form_valid(form)


class BoardingRoomCreateView(CreateView):
    model = BoardingRoom
    form_class = CreateBoardingRoomForm
    template_name = 'property_management/dashboard/property/boarding_room/add_boarding_room.html'
    success_url = reverse_lazy('property_management:create-boarding-room')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['landlord'] = self.request.user
        return kwargs

    def form_valid(self, form):
        boarding_rooms = form.save(commit=True)
        self.object = boarding_rooms[0]  # Get the first boarding room created
        messages.success(self.request, f"{len(boarding_rooms)} Boarding room created successfully.")
        return HttpResponseRedirect(self.get_success_url())


class BoardingHouseUpdateView(UpdateView):
    model = BoardingHouse
    form_class = UpdateBoardingHouseForm
    template_name = 'property_management/dashboard/property/boarding_house/edit_boarding_house.html'
    context_object_name = 'boarding_house'

    def get_success_url(self):
        return reverse_lazy('property_management:update-boarding-house', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_images'] = self.object.get_existing_images()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Boarding house updated successfully.")
        return super().form_valid(form)


class BoardingRoomUpdateView(UpdateView):
    model = BoardingRoom
    form_class = UpdateBoardingRoomForm
    template_name = 'property_management/dashboard/property/boarding_room/edit_boarding_room.html'
    context_object_name = 'boarding_room'

    def get_success_url(self):
        return reverse_lazy('property_management:update-boarding-room', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Boarding room updated successfully.")
        return super().form_valid(form)


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

        # Get the latest booking of the tenant
        if self.request.user.is_authenticated and self.request.user.user_type == 'tenant':
            tenant = self.request.user
            is_room_tenant = self.object.room_tenants.filter(tenant=tenant, check_out_date__isnull=True).exists()

            if is_room_tenant:
                context['flag'] = 'already_rented'
            else:
                latest_booking = self.object.bookings.filter(tenant=tenant).order_by('-created_at').first()
                if latest_booking and latest_booking.is_processing():
                    context['request_booking_form'] = RequestBookingForm(instance=latest_booking,
                                                                         boarding_room=self.object, tenant=tenant)
                    context['flag'] = 'booking_in_progress'
                else:
                    context['request_booking_form'] = RequestBookingForm(boarding_room=self.object, tenant=tenant)

            # Check if the tenant has checked out
            has_checked_out = self.object.room_tenants.filter(tenant=tenant, check_out_date__isnull=False).exists()
            if has_checked_out:
                context['rating_form'] = RatingForm()

        return context

    # TODO: Restrict access to this method to tenant only
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Ensure self.object is set
        context = self.get_context_data()

        if 'request-booking' in request.POST:
            request_booking_form = RequestBookingForm(data=request.POST, boarding_room=self.object, tenant=request.user)
            if request_booking_form.is_valid():
                request_booking_form.save()
                messages.success(request, "Booking request sent successfully.")
                return redirect('property_management:boarding-room', pk=self.object.pk)
            else:
                context['request_booking_form'] = request_booking_form
                return self.render_to_response(context)
        elif 'cancel-booking' in request.POST:
            booking_id = request.POST.get('cancel-booking')
            booking = get_object_or_404(Booking, id=booking_id)

            # Ensure only authorized users can cancel booking
            if booking.tenant != request.user:
                return HttpResponseForbidden("You are not allowed to cancel this booking.")

            booking.status = Booking.Status.CANCELLED
            booking.save()
            messages.success(request, "Booking cancelled successfully.")
            return redirect('property_management:boarding-room', pk=self.object.pk)


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


class BookingListView(ListView):
    model = Booking
    paginator_class = SafePaginator
    context_object_name = 'bookings'
    paginate_by = 10
    template_name = 'property_management/dashboard/booking/booking_list.html'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_bookings'] = self.get_queryset().count()
        context['search_form'] = BookingSearchForm(self.request.GET)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(boarding_room__boarding_house__landlord=self.request.user)
        # Handle search query
        query = self.request.GET.get('query', '')
        search_by = self.request.GET.get('search_by', 'tenant')  # Default to 'name' if not specified
        if query:
            if search_by == 'tenant':
                queryset = queryset.filter(tenant__name_icontains=query)
            elif search_by == 'boarding_room':
                queryset = queryset.filter(boarding_room__name__icontains=query)
            elif search_by == 'boarding_house':
                queryset = queryset.filter(boarding_room__boarding_house__name__icontains=query)

        # Handle sorting with direction (ascending or descending)
        sort_by = self.request.GET.get('sort', '')
        direction = self.request.GET.get('direction', 'asc')  # Default direction is ascending
        if sort_by:
            if sort_by == 'tenant':
                pass
            elif sort_by == 'status':
                pass
            elif sort_by == 'boarding_room':
                pass
            elif sort_by == 'boarding_house':
                pass
            elif sort_by == 'created_at':
                pass

        return queryset

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # Handle approval of a booking
        if 'approve-booking' in request.POST:
            booking_id = request.POST.get('approve-booking')
            booking = get_object_or_404(Booking, id=booking_id)

            if booking.boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to approve this booking.")

            messages.success(request, "Booking approved successfully.")
            # Approve the booking
            booking.status = Booking.Status.APPROVED
            booking.save()
            return redirect('property_management:booking-management')
        # Handle rejection of a booking
        elif 'reject-booking' in request.POST:
            booking_id = request.POST.get('reject-booking')
            booking = get_object_or_404(Booking, id=booking_id)

            if booking.boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to reject this booking.")

            messages.success(request, "Booking rejected successfully.")
            # Reject the booking
            booking.status = Booking.Status.REJECTED
            booking.save()
            return redirect('property_management:booking-management')
        # Handle completion of a booking (check-in)
        elif 'complete-booking' in request.POST:
            booking_id = request.POST.get('complete-booking')
            booking = get_object_or_404(Booking, id=booking_id)

            if booking.boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to complete this booking.")

            with transaction.atomic():
                # Complete the booking
                booking.status = Booking.Status.COMPLETED
                booking.save()

                # Create a BoardingRoomTenant
                BoardingRoomTenant.objects.create(
                    boarding_room=booking.boarding_room,
                    tenant=booking.tenant,
                )

            messages.success(request, "Booking completed successfully.")
            return redirect('property_management:booking-management')

        return self.render_to_response(context)


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'property_management/dashboard/booking/booking_detail.html'
    context_object_name = 'booking'


class RoomTenantListView(ListView):
    model = BoardingRoomTenant
    paginator_class = SafePaginator
    context_object_name = 'room_tenants'
    template_name = 'property_management/dashboard/tenant/tenant_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_room_tenants'] = self.get_queryset().count()
        context['search_form'] = RoomTenantSearchForm(self.request.GET)
        context['tenant_status'] = self.kwargs.get('tenant_status')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(boarding_room__boarding_house__landlord=self.request.user)

        tenant_status = self.kwargs.get('tenant_status')

        if tenant_status == 'checked-in':
            queryset = queryset.filter(check_out_date__isnull=True)
        elif tenant_status == 'checked-out':
            queryset = queryset.filter(check_out_date__isnull=False)

        return queryset

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        # Handle checked-out of a tenant
        if 'check-out-tenant' in request.POST:
            room_tenant_id = request.POST.get('check-out-tenant')

            room_tenant = get_object_or_404(BoardingRoomTenant, id=room_tenant_id)

            if room_tenant.boarding_room.boarding_house.landlord != request.user:
                return HttpResponseForbidden("You are not allowed to checkout this tenant.")

            messages.success(request, "Tenant has been checkout successfully.")
            # Checkout the tenant
            room_tenant.check_out_date = timezone.now()
            room_tenant.save()
            return redirect('property_management:tenant-management')

        return self.render_to_response(context)


class LandlordListView(ListView):
    model = User
    context_object_name = 'landlords'
    template_name = 'property_management/landlords.html'
    paginator_class = SafePaginator
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(user_type=User.Type.LANDLORD)
        return queryset
