from django.contrib.contenttypes.models import ContentType
from django.utils.deprecation import MiddlewareMixin

from . import models

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class CartDoesNotExist(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class StockEmpty(Exception):
    pass


class CartProxy(MiddlewareMixin):
    def __init__(self, request):
        super(CartProxy, self).__init__()
        user = request.user
        try:
            # First search by user
            if not user.is_anonymous():
                cart = models.Cart.objects.get(user=user, checked_out=False)
            # If not, search by request id
            else:
                user = None
                cart_id = request.session.get(CART_ID)
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
        except:
            cart = self.new(request, user=user)

        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    @classmethod
    def get_cart(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            cart = models.Cart.objects.get(id=cart_id, checked_out=False)
        else:
            cart = None
        return cart

    def new(self, request, user=None):
        cart = models.Cart(creation_date=timezone.now(), user=user)
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, stock, unit_price, quantity=1):
        if (stock.stock != -1) and (stock.stock - int(quantity) < 0):
            raise StockEmpty(stock)
        try:
            ctype = ContentType.objects.get_for_model(type(product),
                                                      for_concrete_model=False)
            item = models.Item.objects.get(cart=self.cart,
                                           product=product,
                                           stock=stock,
                                           content_type=ctype)
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.stock_id = stock.pk
            item.save()
        else:
            item.quantity += int(quantity)
            item.save()
        stock.stock -= int(quantity)
        stock.save()
        return item

    def remove_item(self, item_id):
        try:
            item = models.Item.objects.get(cart=self.cart,
                                           id=item_id)
            if item.stock.stock != -1:
                item.stock.stock += item.quantity
                item.stock.save()
            item.delete()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def update(self, id, quantity, *args):
        try:
            item = models.Item.objects.get(cart=self.cart,
                                           id=id)
            prev_qty = item.quantity
            if int(quantity) <= item.stock.stock + prev_qty:
                item.quantity = quantity
                item.save()
                item.stock.stock -= int(quantity) - prev_qty
                item.stock.save()
            else:
                raise StockEmpty('Too many products chosen for {}. Only {} left in stock!'.format(str(item.stock), item.stock.stock))
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        return self.cart

    def delete_old_cart(self, user):
        try:
            cart = models.Cart.objects.get(user=user)
            cart.delete()
        except models.Cart.DoesNotExist:
            pass

    def is_empty(self):
        return self.cart.is_empty()

    def replace(self, cart_id, new_user):
        try:
            self.delete_old_cart(new_user)
            cart = models.Cart.objects.get(pk=cart_id)
            cart.user = new_user
            cart.save()
            return cart
        except models.Cart.DoesNotExist:
            raise CartDoesNotExist

        return None

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def get_item(self, item):
        try:
            obj = models.Item.objects.get(pk=item)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

        return obj

    def get_last_cart(self, user):
        try:
            cart = models.Cart.objects.get(user=user, checked_out=False)
        except models.Cart.DoesNotExist:
            self.cart.user = user
            self.cart.save()
            cart = self.cart

        return cart

    def checkout(self):
        cart = self.cart
        try:
            cart.checked_out = True
            cart.save()
        except models.Cart.DoesNotExist:
            pass

        return cart
