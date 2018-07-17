from django.contrib.contenttypes.models import ContentType
from django.utils.deprecation import MiddlewareMixin
import json

from . import models
from vendor.models import Vendor,Shipping

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

    def add(self, product, vendor, stock, unit_price, quantity=1):
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
            item.vendor_id = vendor.pk
            item.save()
        else:
            item.quantity += int(quantity)
            item.save()
        if stock.stock != -1:
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
            self.recalculate_shipping()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def recalculate_shipping(self):
        # check if only item from specific vendor
        shipping = json.loads(self.cart.shipping)
        items_grouped = self.get_items_by_vendor()
        existent_vendors_ids = [vendor.pk for vendor,items in items_grouped.items()]
        for vendorid in list(shipping.keys()):
            if int(vendorid) not in existent_vendors_ids:
                del shipping[vendorid]
        self.cart.shipping = json.dumps(shipping)
        self.cart.save()


    def update(self, id, quantity, *args):
        try:
            item = models.Item.objects.get(cart=self.cart,
                                           id=id)
            prev_qty = item.quantity
            if (int(quantity) <= item.stock.stock + prev_qty) or item.stock.stock == -1:
                item.quantity = quantity
                item.save()
                if item.stock.stock == -1:
                    item.stock.stock -= int(quantity) - prev_qty
                    item.stock.save()
            else:
                raise StockEmpty('Too many products chosen for {}. Only {} are in stock!'.format(str(item.stock), int(item.stock.stock+item.quantity)))
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        return self.cart

    def update_shipping(self, shipping):
        self.cart.shipping = shipping
        self.cart.save()

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
        self.cart.shipping = ''
        self.cart.save()

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

    def get_shipping(self):
        import json
        res = {}
        if self.cart.shipping != '':
            for vendor,shipping in json.loads(self.cart.shipping).items():
                res[vendor] = Shipping.objects.get(pk=shipping)
        return res

    def get_items_by_vendor(self):
        from collections import defaultdict
        # groups items and shipping by vendors
        items = defaultdict(list)
        for item in self:
            items[item.vendor].append(item)
        return items

    def calculate_total(self):
        total_price = self.cart.total_price()
        shipping = self.get_shipping()
        #add shipping
        for vid, ship in shipping.items():
            total_price += ship.price
        return total_price

    def get_formatted_cart(self):
        #returns items and shipping
        items = self.get_items_by_vendor()
        #group by vendors
        shipping = self.get_shipping()
        grouped_by_vendors = {}
        for vendor,grouped_items in items.items():
            grouped_by_vendors[vendor] = {
                'items': grouped_items,
                'shipping': shipping[str(vendor.pk)]
            }
        return grouped_by_vendors
