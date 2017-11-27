from django.http import JsonResponse
from django.shortcuts import render_to_response
from product.models import Art, Support
from .proxy import CartProxy


def add_to_cart(request, art_id, quantity=1):
    product = Art.objects.get(id=art_id)
    # support = Support.objects.get(id=support_id)
    cart = request.cart
    try:
        cart.add(product, product.unit_price, quantity)
        res = True
    except: #todo handle multiple exceptions
        res = False
    return JsonResponse(dict(result=res))

def remove_from_cart(request, item_id):
    cart = request.cart
    try:
        cart.remove_item(item_id)
        res = True
    except: #todo handle multiple exceptions
        res = False
    return JsonResponse(dict(result=res))


def get_cart(request):
    print("Getting cart...")
    cart = CartProxy(request)
    items = [i for i in cart]
    return render_to_response('cart.html', dict(cart=items))
