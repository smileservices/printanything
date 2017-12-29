from django.http import JsonResponse
from django.shortcuts import render_to_response
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
    return render_to_response('changuito/cart.html', dict(section='Cart', cart=items, cart_total=cart_total))


def update_cart(request):
    if request.method == 'POST':
        cart_proxy = CartProxy(request)
        #todo handle new qty > available stock for art/support
        #todo handle remove item
        #todo handle update qty
        #todo return result: error or result: true



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

