from django.urls import path
from .views import  ReservationListView, ReservationDetailView, ReservationCreateView, ReservationUpdateView, ReservationCancelView
from . import views

urlpatterns = [
    path('reservation/list/', ReservationListView.as_view(), name='reservation-list'),
    path('reservation/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/new/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservation/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('reservation/<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
]