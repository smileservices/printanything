from __future__ import unicode_literals
from django.db import models
from django.utils.crypto import get_random_string


def get_save_path(instance, filename):
    return "vendors/{0}_sizes.{1}".format(
        get_random_string(22),
        filename.split(".")[-1].lower()
    )


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    sizes_chart = models.ImageField(default=None, upload_to=get_save_path)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vendor'


class Size(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Colour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name
