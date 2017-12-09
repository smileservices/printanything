# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from order.models import Order, OrderDetails, ShippingDetails


# Create your views here.

def checkout(request):
    cart = request.cart
    data = {
        'total_price': cart.total_price(),
        'total_quantity': cart.total_quantity()
    }
    return render(request, 'checkout.html', data)


def pay(request):
    return render(request, 'checkout.html')


def place(request):
    return render(request, 'checkout.html')
