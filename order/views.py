# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from order.models import OrderGroup, Order, Payment
from customer.models import Customer
from contact.models import Contact
from changuito.proxy import CartProxy
from tshirtstore import settings
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def checkout(request):
    cart_proxy = CartProxy(request)
    items = []
    cart_total = 0
    for i in cart_proxy:
        items.append(i)
        cart_total += i.total_price
    return render(request, 'order/checkout.html', dict(
        section='Cart',
        cart=cart_proxy.get_formatted_cart(),
        cart_total=cart_proxy.calculate_total(),
    ))


# each cart gets grouped into an order group
def place_order(request):
    cart_proxy = CartProxy(request)
    cart_grouped = cart_proxy.get_formatted_cart()
    customer, contact = __get_customer_contact(request)
    total_amount = cart_proxy.calculate_total()
    # create order group and delete the other that existed in memory and has not been paid
    order_group = OrderGroup(customer=customer, contact=contact, total_amount=total_amount)
    order_group.save()
    for vendor, cart in cart_grouped.items():
        order = Order(order_group=order_group)
        order.save()
        order.place_order(cart['items'], {
            # shipping details
            'type': cart['shipping'].name,
            'cost': cart['shipping'].price,
            'details': request.POST.get('shipping_details', False),
            'status': 'just created',
            'contact': contact
        })
    # redirect to
    return process_payment(request, order_group)


#   order group connects all the split orders into one
#   order group id is sent to paypal and used for referencing the split orders

def process_payment(request, order_group):
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": order_group.total_amount,
        "item_name": order_group.id,
        "custom": order_group.id,
        "invoice": order_group.id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment-return')),
        "cancel_return": request.build_absolute_uri(reverse('payment-cancel')),
    }
    request.session['order_group'] = order_group.id
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/payment_proceed.html", context)


def payment_complete(request):
    cart_proxy = CartProxy(request)
    cart_proxy.clear()
    cart_proxy.cart.delete()
    order_group = OrderGroup.objects.get(pk=request.session['order_group'])
    context = {
        'order_group': order_group,
        'contact': order_group.contact,
    }
    # todo modify template for rendering with order_group
    html_msg = render_to_string('order/email/order_placed/customer_main.html', context=context)
    text_msg = strip_tags(html_msg)
    # send email to customer
    msg = EmailMultiAlternatives('Your order', body=text_msg, from_email='noreply@tshirtstore.com',
                                 to=[order_group.customer.email, ], bcc=__get_admins_email())
    msg.attach_alternative(html_msg, "text/html")
    msg.send()
    # send email to admins

    return render(request, 'payment/payment_complete.html', {
        'section': 'Payment'
    })


def payment_canceled(request):
    # todo delete order group
    return render(request, 'payment/payment_canceled.html', {
        'section': 'Payment'
    })


class PaymentException(Exception):
    pass


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            raise PaymentException('Invalid payment: receiver email does not match!')
        # Retrieve order
        order_group = OrderGroup.objects.get(id=ipn_obj.custom)
        if order_group is None:
            raise PaymentException('Payment received for order_group that doesn\'t exist!')
        if ipn_obj.mc_gross == order_group.calculate_price() and ipn_obj.mc_currency == 'USD':
            # add to valid payments
            payment = Payment(
                id=ipn_obj.txn_id,  # yes?
                type='paypal',
                amount=ipn_obj.mc_gross,
                status='complete',
                date=ipn_obj.payment_date,
                order_group=order_group
            )
            payment.save()
            order_group.status = 'Payment received'
            order_group.save()
        else:
            return
    else:
        pass


valid_ipn_received.connect(show_me_the_money)


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
            country='USA',  # hardcoded
            state=request.POST.get('state', ''),
            city=request.POST['city'],
            address=request.POST['address'],
            phone=request.POST.get('phone', ''),
            zip=request.POST.get('zip', ''),
            primary=True,
        )
        contact.save()
    return customer, contact


def __get_admins_email():
    from django.contrib.auth.models import User
    return [user.email for user in User.objects.filter(is_staff=1).all()]


def test_checkout(request):
    order_group = OrderGroup.objects.get(pk=request.session['order_group'])
    context = {
        'order_group': order_group,
        'contact': order_group.contact,
    }
    return render(request, 'order/email/order_placed/customer_main.html', context)
