from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.db import connections

from .forms import ReservationCreateForm, ReservationUpdateForm
from .models import Reservation


class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservation/reservation_list.html'
    context_object_name = 'reservation'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        reservation_list = Reservation.objects.raw(f"SELECT * FROM reservation WHERE address LIKE '%%{query}%%' OR name LIKE '%%{query}%%'")
        return reservation_list


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation/reservation_detail.html'
    context_object_name = 'reservation'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationCreateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.manager_id = self.request.user.id
        return super().form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationUpdateForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.manager_id = self.request.user.id
        return super().form_valid(form)

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.manager_id


class ReservationCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    template_name = 'reservation/reservation_delete.html'
    success_url = '/'

    def test_func(self):
        reservation = self.get_object()
        return self.request.user.id == reservation.manager_id
