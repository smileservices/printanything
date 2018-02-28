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
from django.views import generic
from admin import views
from vendor.models import Vendor
from django.urls import reverse_lazy

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
    url(r'^users/create$', views.CreateUser.as_view(), name='create_user'),
    url(r'^users/edit/(?P<pk>[\d])', views.UpdateUser.as_view(), name='update_user'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)