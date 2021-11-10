from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.db import connections

from .forms import HotelCreateForm, HotelUpdateForm
from .models import Hotel, Room
from reservation.models import Reservation


class HomePageView(TemplateView):
    model = Hotel
    template_name = 'hotel/home.html'


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'
    context_object_name = 'hotel'

    def get_queryset(self):  # new
        address = self.request.GET.get('address')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        num_people = self.request.GET.get('num_people')

        if address:
            hotel_list = Hotel.objects.raw(f"SELECT * FROM hotel WHERE address LIKE '%%{address}%%' OR name LIKE '%%{address}%%'")
        else:
            hotel_list = Hotel.objects.raw(f"SELECT * FROM hotel")

        hotel_list_ = []
        for hotel in hotel_list:
            hotel_id = hotel.id
            room_list = Room.objects.raw("SELECT * FROM room WHERE hotel_id = %s", [hotel_id])

            room_list_ = []
            for room in room_list:
                res_list = Reservation.objects.raw(f"SELECT * FROM reservation WHERE room_id = '%%{room.id}%%' "
                                                   f"AND (CAST('%%{start_date}%%' AS DATE) <= start_date AND start_date < CAST('%%{end_date}%%' AS DATE)"
                                                   f" OR CAST('%%{start_date}%%' AS DATE) < end_date AND end_date <= CAST('%%{end_date}%%' AS DATE))")
                if not res_list:
                    room_list_.append(room)

            if room_list_:
                hotel_list_.append(hotel)

        return hotel_list_


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'
    context_object_name = 'hotel'


class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    template_name = 'hotel/hotel_form.html'
    form_class = HotelCreateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.manager_id = self.request.user.id
        return super().form_valid(form)


class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    template_name = 'hotel/hotel_form.html'
    form_class = HotelUpdateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.manager_id = self.request.user.id
        return super().form_valid(form)

    def test_func(self):
        hotel = self.get_object()
        return self.request.user.id == hotel.manager_id


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    template_name = 'hotel/hotel_delete.html'
    success_url = '/'

    def test_func(self):
        hotel = self.get_object()
        return self.request.user.id == hotel.manager_id


def about(request):
    return render(request, 'hotel/about.html', {'name': 'about'})
