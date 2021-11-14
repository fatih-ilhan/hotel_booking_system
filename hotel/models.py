from django.db import models
from django.db.models import Q
from django.utils import timezone
from users.models import User
from django.urls import reverse


class Hotel(models.Model):

    id = models.BigIntegerField(blank=True, null=False, primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.BigIntegerField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel'


class Room(models.Model):
    room_no = models.PositiveIntegerField()
    num_people = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'room'


class Reservation(models.Model):

    id = models.BigIntegerField(blank=True, null=False, primary_key=True)
    res_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    room = models.ForeignKey(Room, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'
