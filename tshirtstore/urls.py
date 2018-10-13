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
from tshirtstore import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render

urlpatterns = [

    url(r'^admin/', include('admin.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^products/', include('product.urls')),
    url(r'^cart/', include('changuito.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^pages/(?P<page_name>[-\w]+)/$',views.static_page,name='pages'),
    url(r'^$', views.homepage, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # do we need this?
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
