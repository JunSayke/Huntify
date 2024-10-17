from django.shortcuts import redirect
from django.http import HttpResponseNotAllowed, Http404
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from booking_feature.models import *
from booking_feature.forms import BoardingHouseForm, RoomForm
from utilities.mixin import CustomPermissionRequiredMixin, RefererSuccessUrlMixin, Handle404RedirectMixin
from django.urls import reverse, reverse_lazy

class BoardingHouseCreateView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, CreateView):
    model = BoardingHouse
    form_class = BoardingHouseForm
    template_name = 'boarding_house/add_boarding_house.html'
    permission_required = 'booking_feature.add_boardinghouse'

    def form_valid(self, form):
        form.instance.account_id = self.request.user # Automatically assign the account to the boarding house
        return super().form_valid(form)
    
class BoardingHouseUpdateView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, UpdateView):
    model = BoardingHouse
    pk_url_kwarg = 'boarding_house_id' # This is name of the keyword argument in the URL pattern, Default is 'pk'
    form_class = BoardingHouseForm
    template_name = 'boarding_house/edit_boarding_house.html'
    context_object_name = 'boarding_house'
    permission_required = 'booking_feature.change_boardinghouse'

class BoardingHouseDetailView(Handle404RedirectMixin, DetailView):
    model = BoardingHouse
    pk_url_kwarg = 'boarding_house_id' # This is name of the keyword argument in the URL pattern, Default is 'pk'
    template_name = 'boarding_house/boarding_house_detail.html'
    context_object_name = 'boarding_house'

    def get_404_redirect_url(self):
        return reverse('boarding_house_list')  # Default redirect URL

class BoardingHouseListView(ListView):
    model = BoardingHouse
    template_name = 'boarding_house/boarding_house_list.html'
    context_object_name = 'boarding_houses'

class BoardingHouseDeleteView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, DeleteView):
    model = BoardingHouse
    pk_url_kwarg = 'boarding_house_id'
    permission_required = 'booking_feature.delete_boardinghouse'

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])














class RoomCreateView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'boarding_room/add_room.html'
    permission_required = 'booking_feature.add_room'

    def form_valid(self, form):
        form.instance.boarding_house_id = BoardingHouse.objects.get(id=self.kwargs['boarding_house_id']) # Automatically assign the boarding house to the room
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boarding_house'] = BoardingHouse.objects.get(id=self.kwargs['boarding_house_id'])
        return context
    
class RoomUpdateView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, Handle404RedirectMixin, UpdateView):
    model = Room
    pk_url_kwarg = 'room_id' # This is name of the keyword argument in the URL pattern, Default is 'pk'
    form_class = RoomForm
    template_name = 'boarding_room/edit_room.html'
    context_object_name = 'room'
    permission_required = 'booking_feature.change_room'

    def get_404_redirect_url(self):
        room = self.get_object()
        return reverse('boarding_house_detail', kwargs={'boarding_house_id': room.boarding_house_id.id})

class RoomDetailView(Handle404RedirectMixin, DetailView):
    model = Room
    pk_url_kwarg = 'room_id'
    template_name = 'boarding_room/room_detail.html'
    context_object_name = 'room'

    def get_404_redirect_url(self):
        room = self.get_object()
        return reverse('boarding_house_detail', kwargs={'boarding_house_id': room.boarding_house_id})

class RoomListView(ListView):
    model = Room
    template_name = 'boarding_room/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        boarding_house_id = self.kwargs['boarding_house_id']
        return Room.objects.filter(boarding_house_id=boarding_house_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boarding_house'] = BoardingHouse.objects.get(id=self.kwargs['boarding_house_id'])
        return context
    
class RoomDeleteView(CustomPermissionRequiredMixin, RefererSuccessUrlMixin, DeleteView):
    model = Room
    pk_url_kwarg = 'room_id'
    permission_required = 'booking_feature.delete_room'

    def get_success_url(self):
        room = self.get_object()
        return reverse_lazy('boarding_house_detail', kwargs={'boarding_house_id': room.boarding_house_id.id})


