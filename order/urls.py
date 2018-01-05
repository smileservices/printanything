from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from order import views

urlpatterns = [
    url(r'^checkout', views.checkout, name='checkout'),
    url(r'^place', views.place_order, name='place-order'),
]
