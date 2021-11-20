from django.urls import path
from .views import HomePageView, HotelListView, HotelDetailView, HotelCreateView, HotelUpdateView, HotelDeleteView, \
    ReservationListView, ReservationDetailView, ReservationCreateView, ReservationUpdateView, ReservationCancelView, \
    ReservationRateView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='hotel-home'),
    path('hotel/list/', HotelListView.as_view(), name='hotel-list'),
    path('hotel/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotel/new/', HotelCreateView.as_view(), name='hotel-create'),
    path('hotel/<int:pk>/update/', HotelUpdateView.as_view(), name='hotel-update'),
    path('hotel/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete'),
    path('reservation/list/', ReservationListView.as_view(), name='reservation-list'),
    path('reservation/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/new/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservation/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservation/<int:pk>/delete/', ReservationCancelView.as_view(), name='reservation-cancel'),
    path('reservation/<int:pk>/rate/', ReservationRateView.as_view(), name='reservation-rate'),
    path('about/', views.about, name='hotel-about'),
]
