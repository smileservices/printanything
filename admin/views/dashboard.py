from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings


def dashboard(request):
    if request.user.is_staff:
        return render(request, 'admin/dashboard.html')
    else:
        return redirect(settings.LOGIN_URL)
