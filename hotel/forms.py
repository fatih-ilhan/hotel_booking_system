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
            cursor.execute('SELECT COUNT(*) FROM hotel')
            num_hotel = cursor.fethcone()[0]
            if num_hotel > 0:
                cursor.execute('SELECT LAST_INSERT_ID() INTO @hotel;')
                hotel_id = cursor.fetchone()[0]
            else:
                hotel_id = 0
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
        res_id = self.instance.id
        hotel_id = self.instance.hotel_id

        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        old_start_date = self.instance.start_date
        old_end_date = self.instance.end_date

        with connection.cursor() as cursor:
            cursor.execute('SELECT room_id FROM reserved_room WHERE res_id = %s', [res_id])
            room_id_list = cursor.fetchall()
            cursor.execute('SELECT SUM(num_people) FROM room WHERE id IN %s', [room_id_list])
            num_people = cursor.fetchone()[0]

        num_rooms = len(room_id_list)

        if end_date <= old_start_date or start_date >= old_end_date:
            room_list = filter_rooms(hotel_id, start_date, end_date, num_people, num_rooms)
            available_flag = all([r in [r_.id for r_ in room_list] for r in room_id_list])
        else:
            room_list_ = []
            flag = False

            if start_date < old_start_date:
                room_list = filter_rooms(hotel_id, start_date, old_start_date, num_people, num_rooms)
                room_list_.extend(room_list)
                flag = True

            if end_date > old_end_date:
                room_list = filter_rooms(hotel_id, old_end_date, end_date, num_people, num_rooms)
                room_list_.extend(room_list)
                flag = True

            room_list = list(set(room_list_))

            if not flag:
                available_flag = True
            else:
                available_flag = all([r in [r_.id for r_ in room_list] for r in room_id_list])

        if available_flag:
            reservation = super(ModelForm, self).save(commit=True)
        else:
            reservation = super(ModelForm, self).save(commit=False)

        return reservation


class ReservationRateForm(ModelForm):

    class Meta:
        model = Reservation
        fields = ['rating']

    def save(self, commit=True):
        reservation = super(ModelForm, self).save(commit=True)
        return reservation