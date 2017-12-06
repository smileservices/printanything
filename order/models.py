# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from customer.models import Customer as Customer
from contact.models import Contact
from product.models import Art, Support
from changuito.models import Cart

# Create your models here.


class Order(models.Model):
    date_shipped = models.DateField()
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=255)
    shipping_id = models.CharField(max_length=255)
    ship_to = models.ForeignKey(Contact)

    def place_order(self, cart):
        '''
        :return:
        '''
        #todo convert cart into order

        return self


class OrderDetails(models.Model):
    name = models.CharField(max_length=255)
    order = models.ForeignKey(Order)
    art = models.ForeignKey(Art)
    support = models.ForeignKey(Support)
    unit_price = models.FloatField()
    qty = models.IntegerField()
    subtotal = models.FloatField()

    def set_name(self):
        return

    def calculate_price(self):
        return


class ShippingDetails(models.Model):
    order = models.ForeignKey(Order)
    type = models.CharField(max_length=255)
    cost = models.FloatField()
    details = models.TextField()
    contact = models.ForeignKey(Contact)
