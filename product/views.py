# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core import serializers

from product.models import Art, Support, Tag


# Create your views here.


def detail(request, slug):
    data = {
        'product': get_object_or_404(Art, slug=slug),
        'supports': Support.get_available(),
    }
    return render(request, 'detail/main.html', data)


def support_stock(request, support_id):
    '''
    returns json with stock data for particular support
    :param request:
    :param support_id:
    :return: json
    '''
    support = Support.objects.get(id=support_id)
    stock = support.stock_set.exclude(stock=0).all()
    data = {}
    for item in stock:
        if str(item.colour) not in data:
            data[str(item.colour)] = []
        data[str(item.colour)].append({
            'size': str(item.size),
            'stock': str(item.stock),
            'id': str(item.id),
        })

    return JsonResponse(data)


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