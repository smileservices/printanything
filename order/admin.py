# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderDetails, ShippingDetails, Payment
from contact.models import Contact


class OrderItems(admin.TabularInline):
    model = OrderDetails
    extra = 0

class OrderShipping(admin.TabularInline):
    model = ShippingDetails
    extra = 0

class OrderPayment(admin.TabularInline):
    model = Payment
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('get_id', 'calculate_price', 'placed', 'get_status', 'get_payment_status')
    list_filter = ('placed', 'status__text', 'payment__status')
    inlines = [OrderItems, OrderShipping, OrderPayment]


# Register your models here.
admin.site.register(Order, OrderAdmin)
