from __future__ import unicode_literals
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from api_interface.models import ApiInterface
import os


def get_save_path(instance, filename):
    return "vendors/{0}_sizes.{1}".format(
        get_random_string(22),
        filename.split(".")[-1].lower()
    )


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    sizes_chart = models.ImageField(default=None, upload_to=get_save_path)
    email = models.EmailField()
    api_interface = models.ForeignKey(ApiInterface, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vendor'

    def get_size_chart_url(self):
        return os.path.join(self.sizes_chart.url)

    def place_order(self, order, base_url=None):
        if not self.api:
            return self.place_no_api(order, base_url)
        else:
            return self.api.place(order)

    def place_no_api(self, order, base_url):
        context = {
            'order': order,
            'items': order.orderdetails_set.all(),
            'shipping': order.shippingdetails_set.first(),
            'base_url': base_url
        }
        # return render(request, 'order/email/to_vendor/send_to_vendor.html', context)
        messageHtml = render_to_string('order/email/to_vendor/send_to_vendor.html', context)
        # send email to customer
        msg = EmailMultiAlternatives('New order', body=messageHtml, from_email=settings.EMAIL_ADDRESS_NOTIFICATIONS,
                                     to=[order.vendor.email, ])
        msg.attach_alternative(messageHtml, "text/html")
        for bigImage in order.get_big_pictures():
            msg.attach_file(bigImage.path)
        msg.send()
        return True

class Size(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Colour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=254)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Shipping(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE, db_constraint=False)

    def __str__(self):
        return self.name
