from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
# Create your views here.


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'admin/dashboard.html')
    else:
        return redirect('login')
