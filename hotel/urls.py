from django.urls import path
from .views import HomePageView, HotelListView, HotelDetailView, HotelCreateView, HotelUpdateView, HotelDeleteView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='hotel-home'),
    path('hotel/list/', HotelListView.as_view(), name='hotel-list'),
    path('hotel/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotel/new/', HotelCreateView.as_view(), name='hotel-create'),
    path('hotel/<int:pk>/update/', HotelUpdateView.as_view(), name='hotel-update'),
    path('hotel/<int:pk>/delete/', HotelDeleteView.as_view(), name='hotel-delete'),
    path('about/', views.about, name='hotel-about'),
]