from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.db import connections
from datetime import date
from django.urls import reverse_lazy

from .forms import HotelCreateForm, HotelUpdateForm, ReservationUpdateForm
from .models import Hotel, Reservation, Room


def filter_rooms(hotel_id, start_date, end_date):
    room_list = Room.objects.raw("SELECT * FROM room WHERE hotel_id = %s", [hotel_id])

    room_list_ = []
    for room in room_list:
        res_list = Reservation.objects.raw(f"SELECT * FROM reservation WHERE room_id = '%%{room.id}%%' "
                                           f"AND (CAST('%%{start_date}%%' AS DATE) <= start_date AND start_date < CAST('%%{end_date}%%' AS DATE)"
                                           f" OR CAST('%%{start_date}%%' AS DATE) < end_date AND end_date <= CAST('%%{end_date}%%' AS DATE))")
        if not res_list:
            room_list_.append(room)

    return room_list_


class HomePageView(TemplateView):
    model = Hotel
    template_name = 'hotel/home.html'


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'

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
            room_list_ = filter_rooms(hotel_id, start_date, end_date)

            if room_list_:
                hotel.price = room_list_[0].price
                hotel_list_.append(hotel)

        self.request.res_data = {'start_date': start_date, 'end_date': end_date, 'num_people': num_people}

        return hotel_list_

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['res_data'] = self.request.res_data
        return context


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


class ReservationListView(ListView):
    model = Reservation
    template_name = 'hotel/reservation_list.html'

    def get_queryset(self):  # new
        reservation_list = Reservation.objects.raw(f"SELECT * FROM reservation WHERE customer_id = %s", [self.request.user.id])
        return reservation_list


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'hotel/reservation_detail.html'
    context_object_name = 'reservation'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'hotel/reservation_form.html'
    fields = []

    def form_valid(self, form):
        form.instance.customer_id = self.request.user.id
        form.instance.res_date = date.today()

        start_date = self.request.GET['start_date']
        form.instance.start_date = self.request.GET['start_date']

        end_date = self.request.GET['end_date']
        form.instance.end_date = self.request.GET['end_date']

        room_list = filter_rooms(self.request.GET['hotel_id'], start_date, end_date)
        form.instance.room_id = room_list[0].id
        return super().form_valid(form)

    def get_success_url(self):
        res_list = Reservation.objects.raw(f"SELECT * FROM reservation ORDER BY id DESC LIMIT 1")
        if res_list:
            res_id = res_list[-1].id
        else:
            res_id = 1
        return reverse_lazy('reservation-detail', kwargs={'pk': res_id})


class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    template_name = 'hotel/reservation_update.html'
    form_class = ReservationUpdateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.customer_id

    def get_success_url(self):
        return reverse_lazy('reservation-detail', kwargs={'pk': self.object.id})


class ReservationCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    template_name = 'hotel/reservation_cancel.html'
    success_url = '/'

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.customer_id


def about(request):
    return render(request, 'hotel/about.html', {'name': 'about'})

