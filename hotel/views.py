from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.db import connections

from .forms import HotelCreateForm, HotelUpdateForm
from .models import Hotel, Room


class HomePageView(TemplateView):
    model = Hotel
    template_name = 'hotel/home.html'


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel/hotel_list.html'
    context_object_name = 'hotel'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        hotel_list = Hotel.objects.raw(f"SELECT * FROM hotel WHERE address LIKE '%%{query}%%' OR name LIKE '%%{query}%%'")
        return hotel_list


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
