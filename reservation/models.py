from django.db import models
from django.db.models import Q
from django.utils import timezone
from users.models import User
from hotel.models import Room
from django.urls import reverse


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
