from django import forms
from django.forms import ModelForm
from django.db import connection

from .models import Hotel, Reservation
from .utils.room_utils import filter_rooms


class HotelCreateForm(ModelForm):
    num_rooms_1 = forms.IntegerField()
    price_1 = forms.IntegerField()

    class Meta:
        model = Hotel
        fields = ['name', 'address', 'zip_code', 'phone', 'web_url']

    def save(self, commit=True):
        hotel = super(ModelForm, self).save(commit=True)
        with connection.cursor() as cursor:
            cursor.execute('SELECT LAST_INSERT_ID() INTO @hotel;')  # TODO: if no row exists?
            hotel_id = cursor.fetchone()[0]
            for room_no in range(1, self.cleaned_data['num_rooms_1']+1):
                cursor.execute("INSERT INTO room(room_no, num_people, price, hotel_id) VALUES(%s, %s, %s, %s)",
                               [room_no, 1, self.cleaned_data['price_1'], hotel_id])
        return hotel


class HotelUpdateForm(ModelForm):
    price_1 = forms.IntegerField()

    class Meta:
        model = Hotel
        fields = ['name', 'address', 'zip_code', 'phone', 'web_url']

    def save(self, commit=True):
        hotel = super(ModelForm, self).save(commit=True)
        with connection.cursor() as cursor:
            hotel_id = hotel.id
            cursor.execute("UPDATE room SET price = %s WHERE hotel_id = %s", [self.cleaned_data['price_1'], hotel_id])
        return hotel


class ReservationCreateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'hotel', 'customer']

    def save(self, commit=True):
        reservation = super(ModelForm, self).save(commit=True)
        return reservation


class ReservationUpdateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']

    def save(self, commit=True):
        # TODO: check the availability of new dates, assign new room if necessary
        # room_list_ = filter_rooms(hotel_id, start_date, end_date, num_people, num_rooms)

        reservation = super(ModelForm, self).save(commit=True)
        return reservation


class ReservationRateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['rating']

    def save(self, commit=True):
        reservation = super(ModelForm, self).save(commit=True)
        return reservation