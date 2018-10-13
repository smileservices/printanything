# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from product.models import Art, Tag, Support
# Create your views here.

def homepage(request):
    data = {
        'popular_products': Art.objects.all(),
        'latest_products': Art.objects.all().order_by('dateAdded')[:10],
        'cheapest_support': Support.get_cheapest(),
        'popular_tags': Tag.objects.all()
    }
    return render(request, 'homepage/main.html', data)


def static_page(request,page_name=None):
    return render(request,'static_pages/'+page_name+'.html')
