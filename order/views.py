# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from order.models import Order, OrderDetails, ShippingDetails


# Create your views here.

def checkout(request):
    cart = request.cart.get_cart(request)
    data = {
        'cart': cart
    }
    return render(request, 'order/checkout.html', data)


def pay(request):
    return render(request, 'checkout.html')


def place(request):
    return render(request, 'checkout.html')
