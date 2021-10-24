from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Hotel(models.Model):

    id = models.BigIntegerField(blank=True, null=False, primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.BigIntegerField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    web_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HOTEL'