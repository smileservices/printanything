# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from order.models import Order, OrderDetails, ShippingDetails
from customer.models import Customer
from contact.models import Contact
from changuito.proxy import CartProxy
from shipping.models import Shipping

# Create your views here.

def checkout(request):
    cart_proxy = CartProxy(request)
    items = []
    cart_total = 0
    for i in cart_proxy:
        items.append(i)
        cart_total += i.total_price
    return render(request, 'order/checkout.html', dict(
        section='Cart',
        cart=items,
        cart_total=cart_total,
        shipping_options=Shipping.objects.all()
    ))


def place_order(request):
    cart_proxy = CartProxy(request)
    cart = cart_proxy.get_cart(request)
    customer, contact = __get_customer_contact(request)
    # create order
    order = Order(customer=customer)
    order.save()
    # get shipping costs
    shipping_type, shipping_cost = __get_shipping(request.POST.get('shipping'))
    order.place_order(cart, {
        # shipping details
        'type': shipping_type,
        'cost': shipping_cost,
        'details': request.POST.get('shipping_details', False),
        'status': 'just created',
        'contact': contact
    })
    # redirect to paypal


def payment_complete(request):
    return render(request, 'payment/payment_complete.html', {
        'section': 'Payment'
    })


def __get_customer_contact(request):
    try:
        customer = Customer.objects.get(email=request.POST['email'])
    except Customer.DoesNotExist:
        customer = Customer(email=request.POST['email'])
        customer.save()
    if request.POST.get('contact_id', False):
        contact = Contact.objects.get(id=request.POST['contact_id'])
    else:
        contact = Contact(
            customer=customer,
            name=request.POST['name'],
            country=request.POST['country'],
            state=request.POST.get('state', ''),
            city=request.POST['city'],
            address=request.POST['address'],
            phone=request.POST.get('phone', ''),
            zip=request.POST.get('zip', ''),
            primary=True,
        )
        contact.save()
    return customer, contact


def __get_shipping(id):
    shipping = Shipping.objects.get(id=id)
    return shipping.name, shipping.price
