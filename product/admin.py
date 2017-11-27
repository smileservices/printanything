# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tag, Art, Support

# Register your models here.

admin.site.register(Tag)
admin.site.register(Art)
admin.site.register(Support)
