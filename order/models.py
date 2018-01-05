# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from customer.models import Customer as Customer
from contact.models import Contact
from product.models import Art, Support
from vendor.models import Size, Colour
from changuito.models import Cart

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone
# Create your models here.


class Order(models.Model):
    placed = models.DateTimeField(verbose_name='creation date',
                                         default=timezone.now)
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=255, default='Waiting for payment processor response')

    def place_order(self, cart, shipping_details):
        # convert cart into order
        for item in cart.item_set.all():
            art = item.get_product()
            stock = item.stock
            support = stock.support
            detail = OrderDetails(
                name='{} on {} ({})'.format(str(art), str(support), str(stock)),
                art=art,
                support=support,
                size=stock.size,
                colour=stock.colour,
                unit_price=item.unit_price,
                qty=item.quantity,
                order=self
            )
            detail.save()
        shipping = ShippingDetails(
            order=self,
            type=shipping_details['type'],
            cost=shipping_details['cost'],
            contact=shipping_details['contact'],
            details=shipping_details['details'],
            status=shipping_details['status'],
        )
        shipping.save()
        return self

    def mark_shipped(self):
        return self

    def calculate_price(self):
        return self


class Payment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(max_length=255)
    date = models.DateTimeField()
    order = models.ForeignKey(Order)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=255)
    art = models.ForeignKey(Art)
    support = models.ForeignKey(Support)
    size = models.ForeignKey(Size)
    colour = models.ForeignKey(Colour)
    unit_price = models.FloatField()
    qty = models.IntegerField()

    def calculate_price(self):
        return self.unit_price * self.qty


class ShippingDetails(models.Model):
    order = models.ForeignKey(Order)
    type = models.CharField(max_length=255)
    cost = models.FloatField()
    contact = models.ForeignKey(Contact)
    details = models.TextField()
    status = models.CharField(max_length=255)

    def update_shipping_info(self, *args, **kwargs):
        return self
