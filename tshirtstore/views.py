# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from product.models import Art, Tag, Support
# Create your views here.

def homepage(request):
    data = {
        'popular_products': Art.objects.all(),
        'cheapest_support': Support.get_cheapest(),
        'popular_tags': Tag.objects.all()
    }
    return render(request, 'homepage/main.html', data)
