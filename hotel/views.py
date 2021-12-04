from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import HotelCreateForm, HotelUpdateForm, ReservationUpdateForm, ReservationRateForm
from .models import Hotel, Reservation
from .utils.room_utils import filter_rooms


class HomePageView(TemplateView):
    model = Hotel
    template_name = 'hotel/home.html'


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'

    def get_queryset(self):  # new
        price_dict = {}
        room_dict = {}

        address = self.request.GET.get('address')
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        num_people = int(self.request.GET.get('num_people', '0'))
        num_rooms = int(self.request.GET.get('num_rooms', '0'))

        if self.request.user.is_hotel_manager:
            order_by = self.request.GET.get('order_by', 'name_')
            hotel_list = Hotel.objects.raw(f"SELECT * FROM hotel WHERE (address LIKE '%%{address}%%' OR name LIKE '%%{address}%%') and manager_id = %s ORDER BY name ASC",
                                           [self.request.user.id])
        else:
            order_by = self.request.GET.get('order_by', 'rate_')
            if order_by == 'rate_':
                hotel_list = Hotel.objects.raw(
                    f"SELECT * FROM hotel WHERE address LIKE '%%{address}%%' OR name LIKE '%%{address}%%' ORDER BY rating DESC")
            elif order_by == 'name_':
                hotel_list = Hotel.objects.raw(
                    f"SELECT * FROM hotel WHERE address LIKE '%%{address}%%' OR name LIKE '%%{address}%%' ORDER BY name ASC")
            elif order_by == 'pop__':
                hotel_list = Hotel.objects.raw(
                    f"SELECT * FROM hotel WHERE address LIKE '%%{address}%%' OR name LIKE '%%{address}%%' ORDER BY num_review DESC")
            else:
                hotel_list = Hotel.objects.raw(
                    f"SELECT * FROM hotel WHERE address LIKE '%%{address}%%' OR name LIKE '%%{address}%%'")

        if self.request.user.is_hotel_manager:
            hotel_list_ = hotel_list
        else:
            hotel_list_ = []
            for hotel in hotel_list:
                hotel_id = hotel.id
                room_list_ = filter_rooms(hotel_id, start_date, end_date, num_people, num_rooms)

                if room_list_:
                    hotel.price = sum([r.price for r in room_list_])
                    price_dict[hotel_id] = hotel.price
                    room_dict[hotel_id] = [r.id for r in room_list_]
                    hotel_list_.append(hotel)

        self.request.res_data = {'start_date': start_date, 'end_date': end_date, 'num_people': num_people}
        self.request.session['price_dict'] = price_dict
        self.request.session['room_dict'] = room_dict

        if order_by == 'price':
            prices = [h.price for h in hotel_list_]
            sort_idx = sorted(range(len(prices)), key=prices.__getitem__)
            hotel_list_ = [hotel_list_[i] for i in sort_idx]

        return hotel_list_


def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in the publisher
    context['res_data'] = self.request.res_data
    context['orderby'] = self.request.GET.get('orderby', 'name')

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
        reservation_list = Reservation.objects.raw(f"SELECT * FROM reservation WHERE customer_id = %s",
                                                   [self.request.user.id])
        for i, r in enumerate(reservation_list):
            if r.end_date < date.today():
                reservation_list[i].is_past = True
            else:
                reservation_list[i].is_past = False
        return reservation_list


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'hotel/reservation_detail.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in the publisher

        if self.object.end_date < date.today():
            context['is_past'] = True
        else:
            context['is_past'] = False

        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'hotel/reservation_form.html'
    fields = []

    def form_valid(self, form):
        price_dict = self.request.session['price_dict']
        room_dict = self.request.session['room_dict']

        customer_id = self.request.user.id
        res_date = date.today()
        start_date = self.request.GET['start_date']
        end_date = self.request.GET['end_date']
        hotel_id = self.request.GET['hotel_id']
        price = price_dict[hotel_id]

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reservation(res_date, start_date, end_date, customer_id, hotel_id, price) "
                           "VALUES(%s, %s, %s, %s, %s, %s)",
                           [res_date, start_date, end_date, customer_id, hotel_id, price])

            for room_id in room_dict[hotel_id]:
                cursor.execute('SELECT id FROM reservation ORDER BY id DESC LIMIT 1')
                res_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO reserved_room(res_id, room_id) VALUES(%s, %s)",
                               [res_id, room_id])

        return redirect(self.get_success_url())

    def get_success_url(self):
        res_list = Reservation.objects.raw(f"SELECT * FROM reservation ORDER BY id DESC LIMIT 1")
        if res_list:
            res_id = res_list[-1].id
        else:
            res_id = 1
        return reverse_lazy('reservation-detail', kwargs={'pk': res_id})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['price'] = self.request.session['price_dict'][self.request.GET['hotel_id']]
        return context


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


class ReservationRateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    template_name = 'hotel/reservation_rate.html'
    form_class = ReservationRateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        num_reviews = self.object.hotel.num_review
        rating = self.object.hotel.rating
        new_rating = 0.99 * rating + 0.01 * self.object.rating  # exponential averaging
        with connection.cursor() as cursor:
            cursor.execute("UPDATE hotel SET num_review = %s, rating = %s WHERE id = %s",
                           [num_reviews + 1, new_rating, self.object.hotel.id])
        # form.instance.rating = [int(self.request.POST.get('rating'))]
        return super().form_valid(form)

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.customer_id

    def get_success_url(self):
        return reverse_lazy('reservation-list')


class ReservationCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    template_name = 'hotel/reservation_cancel.html'
    success_url = '/'

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.customer_id


def about(request):
    return render(request, 'hotel/about.html', {'name': 'about'})
