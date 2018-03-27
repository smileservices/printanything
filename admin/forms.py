from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from vendor.models import Vendor
from artist.models import Artist
from product.models import Art, Support
from gallery.models import Image

from admin.widgets import BoostrapCheckbox, BoostrapFileInput


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "is_staff")


class BaseSupportFormSet(forms.BaseInlineFormSet):

    class Meta:
        model = Support
        fields = ("externalId", "slug", "name", "description", "unit_price", "vendor_price")


class VendorForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ("name", "sizes_chart")
        widgets = {
            'sizes_chart': BoostrapFileInput
        }


class SupportForm(forms.ModelForm):

    class Meta:
        model = Support
        fields = ("externalId", "slug", "name", "description", "unit_price", "vendor_price", "vendor")


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("name",)


class BaseImageFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = Image
        fields = ("relative_path", "primary")


class ArtForm(forms.ModelForm):

    ImagesFormSet = forms.inlineformset_factory(
        Art,
        Image,
        formset=BaseImageFormSet,
        fields=["relative_path", "primary"],
        extra=1,
        widgets={
            "primary": BoostrapCheckbox(attrs={'field_name': 'Primary'}),
            "relative_path": BoostrapFileInput,
        }
    )

    class Meta:
        model = Art
        fields = ("externalId", "slug", "name", "big_image", "description", "unit_price", "stock", "artist", "tags")
