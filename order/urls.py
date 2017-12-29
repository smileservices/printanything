from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from order import views

urlpatterns = [
    url(r'^checkout', views.checkout, name='checkout'),
    url(r'^pay', views.pay, name='order-pay'),
    url(r'^place', views.place, name='order-place'),
]
