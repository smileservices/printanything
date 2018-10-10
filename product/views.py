# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core import serializers
from gallery.models import Gallery
from product.models import Art, Support, Tag


# Create your views here.


def detail(request, slug):
    product = get_object_or_404(Art, slug=slug);
    data = {
        'product': product,
        'supports': Support.get_available(),
    }
    return render(request, 'product/detail.html', data)


def support_stock(request, support_id):
    '''
    returns json with stock data for particular support
    :param request:
    :param support_id:
    :return: json
    '''

    support = Support.objects.get(id=support_id)
    stock = support.stock_set.exclude(stock=0).all()
    data = {
        'shipping': [{'id': ship.id, 'name': ship.name, 'price': ship.price, 'description': ship.description} for ship in support.vendor.shipping_set.all()],
        'colours': {},
        'mockup_images': [{"primary": img.primary, "url": img.get_image_url(), "thumb": img.get_thumb_small_url(), "print_area": img.print_area} for img in support.images.all()],
        'gallery': [{"url": img.get_image_url(), "thumb": img.get_thumb_small_url()} for img in Gallery.get_gallery('support', support.id)],
        'sizes_chart': support.vendor.sizes_chart.url
    }


    # group available sizez by colours
    for item in stock:
        if str(item.colour) not in data['colours']:
            data['colours'][str(item.colour)] = {
                'sizes': [],
                'hex_code': item.colour.hex_code
            }
        data['colours'][str(item.colour)]['sizes'].append({
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
    return render(request, 'product/list.html', data)
