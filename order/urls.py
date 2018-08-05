from django.conf.urls import url, include
from django.urls import reverse
from django.contrib import admin
from order import views

urlpatterns = [
    url(r'^checkout', views.checkout, name='checkout'),
    url(r'^test-invoice', views.test_invoice),
    url(r'^order-details/(?P<hash>[-\w]+)', views.show_order_group_status, name='order-details'),
    url(r'^place', views.place_order, name='place-order'),
    url(r'^paypal/', include('paypal.standard.ipn.urls'), name='paypal-ipn'),
    url(r'payment-return', views.payment_complete, name='payment-return'),
    url(r'payment-cancel', views.payment_canceled, name='payment-cancel'),
]
