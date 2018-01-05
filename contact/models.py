# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# not sure if we should use the generic user instead of customer class
from customer.models import Customer as Customer


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)
