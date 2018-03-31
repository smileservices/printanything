"""tshirtstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings
from django.urls import reverse_lazy

from admin import views
from django.views import generic

from vendor.models import Vendor
from artist.models import Artist
from product.models import Art, Support
from order.models import Order, OrderStatus

urlpatterns = [
    url(r'^login/$', auth_views.login, {
        'template_name': 'admin/login.html',
    }, name='admin-login'),
    url(r'^logout/$', auth_views.logout, {
        'next_page': '/'
    }, name='logout'),
    url(r'^$', views.dashboard, name="admin-dashboard"),
    #todo add reset
]

# USERS
urlpatterns += [
    url(r'^users/create$', views.CreateUser.as_view(), name='create-user'),
    url(r'^users/edit/(?P<pk>[\d])', views.UpdateUser.as_view(), name='update-user'),
    url(r'^users/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=User,
        success_url=reverse_lazy('admin-users')
    ), name="delete-user"),
    url(r'^users', generic.ListView.as_view(
        queryset=User.objects.all(),
        template_name='admin/user/list.html'
    ), name='admin-users'),
]

# VENDORS
urlpatterns += [
    url(r'^vendors/create$', views.CreateVendor.as_view(), name='create-vendor'),
    url(r'^vendors/edit/(?P<pk>[\d])', views.UpdateVendor.as_view(), name='update-vendor'),
    url(r'^vendors/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=Vendor,
        success_url=reverse_lazy('admin-vendors')
    ), name='delete-vendor'),
    url(r'^vendors', generic.ListView.as_view(
        queryset=Vendor.objects.all(),
        template_name='admin/vendor/list.html'
    ), name='admin-vendors'),
]

# ARTISTS
urlpatterns += [
    url(r'^artists/create$', views.CreateArtist.as_view(), name='create-artist'),
    url(r'^artists/edit/(?P<pk>[\d])', views.UpdateArtist.as_view(), name='update-artist'),
    url(r'^artists/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=Artist,
        success_url=reverse_lazy('admin-artists')
    ), name='delete-artist'),
    url(r'^artists', generic.ListView.as_view(
        queryset=Artist.objects.all(),
        template_name='admin/artist/list.html'
    ), name='admin-artists'),
]

# ART
urlpatterns += [
    url(r'^art/create$', views.CreateArt.as_view(), name='create-art'),
    url(r'^art/edit/(?P<pk>[\d])', views.UpdateArt.as_view(), name='update-art'),
    url(r'^art/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=Art,
        success_url=reverse_lazy('admin-art')
    ), name='delete-art'),
    url(r'^art', generic.ListView.as_view(
        queryset=Art.objects.all(),
        template_name='admin/art/list.html'
    ), name='admin-art'),
]

# SUPPORTS
urlpatterns += [
    url(r'^supports/create$', views.CreateSupport.as_view(), name='create-support'),
    url(r'^supports/edit/(?P<pk>[\d])', views.UpdateSupport.as_view(), name='update-support'),
    url(r'^supports/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=Support,
        success_url=reverse_lazy('admin-supports')
    ), name='delete-support'),
    url(r'^supports', generic.ListView.as_view(
        queryset=Support.objects.all(),
        template_name='admin/support/list.html'
    ), name='admin-supports'),
]

# ORDER STATUSES
urlpatterns += [
    url(r'^orders/statuses', generic.ListView.as_view(
        queryset=OrderStatus.objects.all(),
        template_name='admin/order/statuses-list.html'
    ), name='order-statuses'),
    url(r'^order/status/delete/(?P<pk>[\d])', generic.DeleteView.as_view(
        model=OrderStatus,
        success_url=reverse_lazy('order-statuses')
    ), name="delete-order-status"),
    url(r'orders/status/edit/(?P<pk>[\d])', views.OrderStatusUpdate.as_view(), name="order-status-edit"),
    url(r'orders/status/create', views.OrderStatusCreate.as_view(), name="order-status-create")
]

# ORDERS
urlpatterns += [
    url(r'^orders', generic.ListView.as_view(
        queryset=Order.objects.all(),
        template_name='admin/order/list.html'
    ), name='admin-orders'),
    url(r'^order/view/(?P<pk>[\d])', views.OrderView.as_view(), name="admin-order-view")
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

