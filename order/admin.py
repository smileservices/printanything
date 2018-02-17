# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderDetails, ShippingDetails
from contact.models import Contact


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('get_id', 'calculate_price', 'placed', 'get_status')
    list_filter = ('placed', 'status__text')


class OrderItems(admin.TabularInline):
    model = OrderDetails
    extra = 0


class OrderShipping(admin.TabularInline):
    model = ShippingDetails
    extra = 0


class OrderItemsAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItems, ]


class OrderShippingAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderShipping, ]


# Register your models here.
admin.site.register(Order, OrderAdmin)
