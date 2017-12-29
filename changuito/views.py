import json
from django.http import JsonResponse
from django.shortcuts import render
from product.models import Art, Support, Stock
from .proxy import CartProxy, ItemDoesNotExist, StockEmpty

def add_to_cart(request):
    if request.method == 'POST':
        product = Art.objects.get(id=request.POST['product_id'])
        quantity = int(request.POST['qty'])
        stock = Stock.objects.get(id=request.POST['stock'])
        cart = request.cart
        price = product.unit_price + stock.support.unit_price
        try:
            cart.add(product, stock, price, quantity)
            res = 'Successfully selected product to your shopping cart!'
        except ItemDoesNotExist:
            res = 'Something went very wrong! The selected product could not be added to your cart because it doesn\'t exist!'
        except StockEmpty as e:
            res = 'We\'re sorry, but it seems that the requested {}\'s stock is empty!'.format(str(e))
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
    cart_proxy = CartProxy(request)
    items = []
    cart_total = 0
    for i in cart_proxy:
        items.append(i)
        cart_total += i.total_price
    return render(request, 'changuito/cart.html', dict(section='Cart', cart=items, cart_total=cart_total))


def update_cart(request):
    if request.method == 'POST':
        #return result: error or result: true
        cart_proxy = CartProxy(request)
        try:
            for item_id, qty in json.loads(request.POST['qty']).items():
                cart_proxy.update(item_id, qty)
            for item_id in json.loads(request.POST['remove']):
                cart_proxy.remove_item(item_id)
            result = True
        except StockEmpty as e:
            result = str(e)
        except ItemDoesNotExist as e:
            result = 'Something went wrong! An item you submitted does not exist in the cart!'
        return JsonResponse(dict(result=result))



def get_cart_json(request):
    cart = CartProxy(request)
    items_list = []
    total = cart.get_cart(request).total_price()
    total_qty = cart.get_cart(request).total_quantity()
    for item in cart:
        items_list.append({
            'name': item.product.name,
            'support': item.stock.support.name + ' - ' + str(item.stock),
            'photo': item.product.get_primary_image().get_thumb_small_url(),
            'url': item.product.get_absolute_url(),
            'qty': int(item.quantity),
            'price': item.unit_price,
            'id': item.id
        })
    return JsonResponse({
        'items': items_list,
        'total_qty': int(total_qty),
        'total': total
    })

