from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from booking_feature.models import *
from booking_feature.forms import BoardingHouseForm, RoomForm

class BoardingHouseCreateView(CreateView):
    model = BoardingHouse
    form_class = BoardingHouseForm
    template_name = 'add_boarding_house.html'
    success_url = reverse_lazy('add_boarding_house')

    def form_valid(self, form):
        form.instance.account_id = self.request.user
        return super().form_valid(form)
    
class BoardingHouseUpdateView(UpdateView):
    model = BoardingHouse
    pk_url_kwarg = 'boarding_house_id' # This is name of the keyword argument in the URL pattern, Default is 'pk'
    form_class = BoardingHouseForm
    template_name = 'edit_boarding_house.html'
    success_url = reverse_lazy('home')

class BoardingHouseDetailView(DetailView):
    model = BoardingHouse
    pk_url_kwarg = 'boarding_house_id' # This is name of the keyword argument in the URL pattern, Default is 'pk'
    template_name = 'boarding_house_detail.html'
    context_object_name = 'boarding_house'

class BoardingHouseListView(ListView):
    model = BoardingHouse
    template_name = 'boarding_house_list.html'
    context_object_name = 'boarding_houses'

class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'add_room.html'
    success_url = reverse_lazy('add_room')

    def form_valid(self, form):
        form.instance.boarding_house_id = BoardingHouse.objects.get(id=self.kwargs['boarding_house_id'])
        return super().form_valid(form)
    
    
