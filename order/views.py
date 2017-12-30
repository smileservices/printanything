# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from order.models import Order, OrderDetails, ShippingDetails
from changuito.proxy import CartProxy


# Create your views here.

def checkout(request):
    cart_proxy = CartProxy(request)
    items = []
    cart_total = 0
    for i in cart_proxy:
        items.append(i)
        cart_total += i.total_price
    return render(request, 'order/checkout.html', dict(section='Cart', cart=items, cart_total=cart_total))
