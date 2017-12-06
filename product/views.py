# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from product.models import Art, Support, Tag
# Create your views here.


def detail(request, slug):
    product = get_object_or_404(Art, slug=slug)
    supports = Support.objects.all()
    data = {
        'product': product,
        'supports': supports
    }
    return render(request, 'detail.html', data)


def search(request, term):
    tags = Tag.objects.filter(name__icontains=term)
    products = {}
    for t in tags:
         for art in t.art_set.all():
             if art.id not in products: products[art.id] = art
    data = {
        'products': products
    }
    return render(request, 'list.html', data)

