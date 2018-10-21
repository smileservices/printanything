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

from admin import generic_views
from admin.views import dashboard, user, vendor, api_interface, support, shipping, artist, art, order

from vendor.models import Vendor
from api_interface.models import ApiInterface
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
    url(r'^$', dashboard.dashboard, name="admin-dashboard"),
    #todo add reset
]

# USERS
urlpatterns += [
    url(r'^users/create$', user.CreateUser.as_view(), name='create-user'),
    url(r'^users/edit/(?P<pk>\d+)', user.UpdateUser.as_view(), name='update-user'),
    url(r'^users/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=User,
        success_url=reverse_lazy('admin-users')
    ), name="delete-user"),
    url(r'^users', generic_views.ListView.as_view(
        queryset=User.objects.all(),
        template_name='admin/user/list.html'
    ), name='admin-users'),
]

# VENDORS
urlpatterns += [
    url(r'^vendors/create$', vendor.CreateVendor.as_view(), name='create-vendor'),
    url(r'^vendors/edit/(?P<pk>\d+)', vendor.UpdateVendor.as_view(), name='update-vendor'),
    url(r'^vendors/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=Vendor,
        success_url=reverse_lazy('admin-vendors')
    ), name='delete-vendor'),
    url(r'^vendors', generic_views.ListView.as_view(
        queryset=Vendor.objects.all(),
        template_name='admin/vendor/list.html'
    ), name='admin-vendors'),
]

# API INTERFACES
urlpatterns += [
    url(r'^api-interface/create$', api_interface.Create.as_view(), name='create-api_interface'),
    url(r'^api-interface/edit/(?P<pk>\d+)', api_interface.Update.as_view(), name='update-api_interface'),
    url(r'^api-interface/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=ApiInterface,
        success_url=reverse_lazy('admin-api-interface')
    ), name='delete-api_interface'),
    url(r'^api-interface', generic_views.ListView.as_view(
        queryset=ApiInterface.objects.all(),
        template_name='admin/api_interface/list.html'
    ), name='admin-api_interface'),
]

# SHIPPING
urlpatterns += [
    url(r'^vendor/(?P<vendor>\d+)/shipping/create', shipping.VendorShippingCreate.as_view(), name='create-shipping'),
    url(r'^shipping/edit/(?P<pk>\d+)', shipping.VendorShippingUpdate.as_view(), name='update-shipping'),
    url(r'^shipping/delete/(?P<pk>\d+)', shipping.VendorShippingDelete.as_view(), name='delete-shipping')
]

# ARTISTS
urlpatterns += [
    url(r'^artists/create$', artist.CreateArtist.as_view(), name='create-artist'),
    url(r'^artists/edit/(?P<pk>\d+)', artist.UpdateArtist.as_view(), name='update-artist'),
    url(r'^artists/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=Artist,
        success_url=reverse_lazy('admin-artists')
    ), name='delete-artist'),
    url(r'^artists', generic_views.ListView.as_view(
        queryset=Artist.objects.all(),
        template_name='admin/artist/list.html'
    ), name='admin-artists'),
]

# ART
urlpatterns += [
    url(r'^art/create$', art.CreateArt.as_view(), name='create-art'),
    url(r'^art/edit/(?P<pk>\d+)', art.UpdateArt.as_view(), name='update-art'),
    url(r'^art/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=Art,
        success_url=reverse_lazy('admin-art')
    ), name='delete-art'),
    url(r'^art', generic_views.ListView.as_view(
        queryset=Art.objects.all(),
        template_name='admin/art/list.html'
    ), name='admin-art'),
]

# SUPPORTS
urlpatterns += [
    url(r'^vendor/(?P<vendorid>\d+)/supports/create$', support.CreateSupport.as_view(), name='create-support'),
    url(r'^supports/edit/(?P<pk>\d+)', support.UpdateSupport.as_view(), name='update-support'),
    url(r'^supports/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=Support,
        success_url=reverse_lazy('admin-supports')
    ), name='delete-support'),
    url(r'^supports', generic_views.ListView.as_view(
        queryset=Support.objects.all(),
        template_name='admin/support/list.html'
    ), name='admin-supports'),
]

# ORDER STATUSES
urlpatterns += [
    url(r'^orders/statuses', generic_views.ListView.as_view(
        queryset=OrderStatus.objects.all(),
        template_name='admin/order/statuses-list.html'
    ), name='order-statuses'),
    url(r'^order/status/delete/(?P<pk>\d+)', generic_views.DeleteView.as_view(
        model=OrderStatus,
        success_url=reverse_lazy('order-statuses')
    ), name="delete-order-status"),
    url(r'orders/status/edit/(?P<pk>\d+)', order.OrderStatusUpdate.as_view(), name="order-status-edit"),
    url(r'orders/status/create', order.OrderStatusCreate.as_view(), name="order-status-create")
]

# ORDERS
urlpatterns += [
    url(r'^orders-closed', generic_views.ListView.as_view(
        queryset=Order.objects.filter(closed=True),
        template_name='admin/order/list.html'
    ), name='admin-orders-closed'),
    url(r'^orders', generic_views.ListView.as_view(
        queryset=Order.objects.filter(closed=False),
        template_name='admin/order/list.html'
    ), name='admin-orders'),
    url(r'^order/view/(?P<pk>\d+)', order.OrderView.as_view(), name="admin-order-view"),
    url(r'^order/update/(?P<pk>\d+)', order.order_update, name="admin-order-update"),
    url(r'^order/process/(?P<pk>\d+)', order.order_process, name="admin-order-process")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

