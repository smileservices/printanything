# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tag, Art, Support, Stock
from gallery.models import Image

# Register your models here.

admin.site.register(Tag)


# ART ADMIN SECTION
class ArtImage(admin.TabularInline):
    model = Image
    extra = 1


class ArtAdmin(admin.ModelAdmin):
    model = Art
    inlines = [ArtImage, ]


admin.site.register(Art, ArtAdmin)


# SUPPORT ADMIN SECTION
class StockAdminInline(admin.TabularInline):
    model = Stock
    extra = 1


class SupportAdmin(admin.ModelAdmin):
    model = Support
    inlines = [StockAdminInline, ]


admin.site.register(Support, SupportAdmin)
