from django.contrib import admin
from .models import Vendor, Colour, Size


# Register your models here.
class SizeAdminInline(admin.TabularInline):
    model = Size
    extra = 1

class ColourAdminInline(admin.TabularInline):
    model = Colour
    extra = 1


class VendorAdmin(admin.ModelAdmin):
    model = Vendor
    inlines = [SizeAdminInline, ColourAdminInline]


admin.site.register(Vendor, VendorAdmin)
