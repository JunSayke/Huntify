from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from booking_feature.models import BoardingHouse
from booking_feature.forms import BoardingHouseForm

class BoardingHouseCreateView(CreateView):
    model = BoardingHouse
    form_class = BoardingHouseForm
    template_name = 'add_boarding_house.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.account_id = self.request.user
        return super().form_valid(form)
    
class BoardingHouseUpdateView(UpdateView):
    model = BoardingHouse
    form_class = BoardingHouseForm
    template_name = 'edit_boarding_house.html'
    success_url = reverse_lazy('home')

class BoardingHouseDetailView(DetailView):
    model = BoardingHouse
    template_name = 'boarding_house_detail.html'
    context_object_name = 'boarding_house'
