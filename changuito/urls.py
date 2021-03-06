from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from changuito import views

urlpatterns = [
    url(r'^buy', views.add_to_cart, name='cart-add'),
    url(r'^remove/(?P<item_id>[-\w]+)', views.remove_from_cart, name='cart-remove'),
    url(r'retrieve', views.get_cart_json, name='cart-inspect-json'),
    url(r'update', views.update_cart, name='update-cart'),
    url(r'^', views.get_cart, name='cart-inspect')
]
