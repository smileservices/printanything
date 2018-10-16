from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from product import views

urlpatterns = [
    url(r'^list', views.list, name='products-list'),
    url(r'^search/(?P<search_term>[-\w]+)', views.search, name='products-search'),
    url(r'^get_support/(?P<support_id>\d+)', views.support_stock, name='support-stock'),
    url(r'^(?P<slug>[-\w]+)', views.detail, name='product-detail'),
]
