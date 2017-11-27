from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from product import views

urlpatterns = [
    url(r'^search/(?P<term>[-\w]+)', views.search, name='products-search'),
    url(r'^(?P<slug>[-\w]+)', views.detail, name='product-detail'),
]
