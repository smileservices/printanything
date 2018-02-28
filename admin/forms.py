from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from vendor.models import Vendor


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "is_staff")


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ("name", "sizes_chart")
