from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from vendor.models import Vendor, Size, Colour
from api_interface.models import ApiInterface
from artist.models import Artist
from product.models import Art, Support, Stock
from gallery.models import SupportImage

from admin.widgets import BoostrapCheckbox, BoostrapFileInput, ColorInput, HiddenInput


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "is_staff")


class BaseStockFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = Stock
        fields = ("stock", "colour", "size")


class BaseSizeFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = Size
        fields = ("name",)


class BaseColourFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = Colour
        fields = ("name", "hex_code")


class VendorForm(forms.ModelForm):
    api_interface = forms.ModelChoiceField(queryset=ApiInterface.objects.all(),empty_label='No API',required=False)
    SizeFormset = forms.inlineformset_factory(
        Vendor,
        Size,
        formset=BaseSizeFormSet,
        extra=1,
        fields=("name",)
    )
    ColourFormset = forms.inlineformset_factory(
        Vendor,
        Colour,
        formset=BaseColourFormSet,
        extra=1,
        fields=("name", "hex_code")
    )

    class Meta:
        model = Vendor
        fields = ("name", "email", "sizes_chart", "api_interface")
        widgets = {
            'sizes_chart': BoostrapFileInput,
        }


class BaseProductImageFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = SupportImage
        fields = ("relative_path", "primary", 'print_area')


class SupportForm(forms.ModelForm):
    ProductImageFormSet = forms.inlineformset_factory(
        Support,
        SupportImage,
        formset=BaseProductImageFormSet,
        extra=1,
        fields=("relative_path", "primary", 'print_area'),
        widgets={
            "primary": BoostrapCheckbox(attrs={'field_name': 'Primary'}),
            "relative_path": BoostrapFileInput,
            "print_area": HiddenInput,
        }
    )

    class Meta:
        model = Support
        fields = ("externalId", "slug", "name", "description", "unit_price", "vendor_price", "vendor")


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ("name",)


class ApiInterfaceForm(forms.ModelForm):
    class Meta:
        model = ApiInterface
        fields = ("name", "endpoint", "api_user", "api_key", "adapter")


class ArtForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = (
        "externalId", "slug", "name", "big_image", "description", "unit_price", "stock", "artist", "tags", "mock_image")
