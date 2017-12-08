from django.http import JsonResponse
from django.shortcuts import render_to_response
from product.models import Art, Support, Size
from .proxy import CartProxy


def add_to_cart(request):
    if request.method == 'POST':
        product = Art.objects.get(id=request.POST['product'])
        quantity = int(request.POST['qty'])
        size = Size.objects.get(id=request.POST['size'])
        cart = request.cart
        price = product.unit_price + size.support.unit_price
        try:
            cart.add(product, size, price, quantity)
            res = True
        except:  # todo handle multiple exceptions
            res = False
        return JsonResponse(dict(result=res))


def remove_from_cart(request, item_id):
    cart = request.cart
    try:
        cart.remove_item(item_id)
        res = True
    except:  # todo handle multiple exceptions
        res = False
    return JsonResponse(dict(result=res))


def get_cart(request):
    cart = CartProxy(request)
    items = [i for i in cart]
    return render_to_response('cart.html', dict(cart=items))
