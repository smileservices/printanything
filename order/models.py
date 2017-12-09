# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from customer.models import Customer as Customer
from contact.models import Contact
from product.models import Art, Support, Size
from changuito.models import Cart

# Create your models here.


class Order(models.Model):
    placed = models.DateTimeField()
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)

    def place_order(self, cart):
        #todo convert cart into order

        return self

    def mark_shipped(self):
        return self


class OrderDetails(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=255)
    art = models.ForeignKey(Art)
    support = models.ForeignKey(Support)
    size = models.ForeignKey(Size)
    unit_price = models.FloatField()
    qty = models.IntegerField()
    subtotal = models.FloatField()

    def calculate_price(self):
        return self.subtotal


class ShippingDetails(models.Model):
    order = models.ForeignKey(Order)
    type = models.CharField(max_length=255)
    cost = models.FloatField()
    contact = models.ForeignKey(Contact)
    details = models.TextField()
    status = models.CharField(max_length=255)

    def update_shipping_info(self, *args, **kwargs):
        return self
