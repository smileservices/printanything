# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from customer.models import Customer as Customer
from contact.models import Contact
from product.models import Art, Support
from vendor.models import Size, Colour
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


# Create your models here.


class OrderStatus(models.Model):
    text = models.CharField(max_length=255, default="unprocessed")

    def __str__(self):
        return self.text.title()


class OrderGroup(models.Model):
    placed = models.DateTimeField(verbose_name='creation date',
                                  default=timezone.now)
    customer = models.ForeignKey(Customer)
    contact = models.ForeignKey(Contact)
    total_amount = models.FloatField()

    def calculate_total(self):
        total = 0
        for order in self.order_set:
            total += order.calculate_price()
        return total

    def get_payment_status(self):
        try:
            return self.payment_set.get().status.upper()
        except ObjectDoesNotExist:
            return "No payment info"

    get_payment_status.short_description = 'Payment Status'


class Order(models.Model):
    status = models.ForeignKey(OrderStatus, default=1)
    info = models.TextField(default="")
    # field for grouping orders for multiple vendors split orders
    order_group = models.ForeignKey(OrderGroup)

    def place_order(self, items, shipping_details):
        # convert cart into order
        for item in items:
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
        self.status = 'Shipped'
        self.save()
        shipping = self.shippingdetails_set.get()
        shipping.status = 'Shipped'
        shipping.save()
        return self

    def calculate_price(self):
        total_price = 0
        for item in self.orderdetails_set.all():
            total_price += item.calculate_price()
        # add shipping cost
        total_price += self.shippingdetails_set.get().cost
        return total_price

    def get_status(self):
        return self.status.text.title()

    def get_orderdetails(self):
        return self.orderdetails_set.all()

    def get_id(self):
        return self.id

    get_id.short_description = 'ID'
    calculate_price.short_description = 'Price'
    get_status.short_description = 'Status'


class Payment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(max_length=128, verbose_name="Payment Status")
    date = models.DateTimeField()
    order_group = models.ForeignKey(OrderGroup)


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
        # todo
        return self
