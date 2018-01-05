from django.conf.urls import url
from django.contrib import admin
from customer import views

urlpatterns = [
    url(r'^email', views.check_email, name='check-user'),
]
