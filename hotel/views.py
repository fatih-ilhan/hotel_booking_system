from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from .models import Hotel


class HomePageView(TemplateView):
    model = Hotel
    template_name = 'hotel/home.html'


class HotelListView(ListView):
    model = Hotel
    # template_name = 'hotel_list.html'
    context_object_name = 'hotel'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        hotel_list = Hotel.objects.raw(f"SELECT * FROM HOTEL WHERE address LIKE '%%{query}%%' OR name LIKE '%%{query}%%'")
        return hotel_list


class HotelDetailView(DetailView):
    model = Hotel


class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    fields = ['name', 'web_url']

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class HotelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hotel
    fields = ['name', 'web_url']

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

    def test_func(self):
        hotel = self.get_object()
        return self.request.user == hotel.manager


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hotel
    success_url = '/'

    def test_func(self):
        hotel = self.get_object()
        return self.request.user == hotel.manager


def about(request):
    return render(request, 'hotel/about.html', {'name': 'about'})
