# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tag, Art, Support, Size
from gallery.models import Image


# Register your models here.


class ArtImage(admin.TabularInline):
    model = Image
    extra = 1


class ArtAdmin(admin.ModelAdmin):
    inlines = [ArtImage, ]


class SupportSize(admin.TabularInline):
    model = Size
    extra = 3


class SupportAdmin(admin.ModelAdmin):
    inlines = [SupportSize, ]


admin.site.register(Tag)
admin.site.register(Support, SupportAdmin)
admin.site.register(Art, ArtAdmin)
