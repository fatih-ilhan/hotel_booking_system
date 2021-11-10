from django import forms
from django.forms import ModelForm
from django.db import connection

from .models import Reservation


class ReservationCreateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['name', 'address', 'zip_code', 'phone', 'web_url']

    def save(self, commit=True):
        reservation = super(ModelForm, self).save(commit=True)
        return reservation


class ReservationUpdateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['name', 'address', 'zip_code', 'phone', 'web_url']

    def save(self, commit=True):
        reservation = super(ModelForm, self).save(commit=True)
        return reservation