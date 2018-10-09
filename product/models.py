# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from PIL import Image as PIL_Image

from django.dispatch import receiver
from django.utils.text import slugify
from vendor.models import Vendor, Size, Colour
from artist.models import Artist
from django.urls import reverse
from gallery.thumbed_image import ThumbedModel


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'


def set_path_art_big(instance, filename):
    return "art/{0}/{1}.{2}".format(
        instance.artist.id,
        "big_" + instance.slug,
        filename.split(".")[-1].lower()
    )


def set_path_art_mock(instance, filename):
    return "art/{0}/{1}.{2}".format(
        instance.artist.id,
        "mock_" + instance.slug,
        filename.split(".")[-1].lower()
    )


class Art(ThumbedModel, models.Model):
    externalId = models.CharField(max_length=64)
    slug = models.SlugField(default='xxx', unique=True)
    name = models.CharField(max_length=64)
    big_image = models.ImageField(upload_to=set_path_art_big, blank=True)
    mock_image = models.ImageField(upload_to=set_path_art_mock, blank=True)
    description = models.TextField()
    unit_price = models.FloatField(default=0.0, verbose_name='Unit Price')
    stock = models.IntegerField()
    artist = models.ForeignKey(Artist)
    dateAdded = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Art.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def get_primary_image(self):
        return self.mock_image

    class Meta:
        verbose_name = 'Art'

    class ThumbProperties:
        image_field_name = 'mock_image'
        thumb_sizes = {'small': (300, 600), 'med': (600, 900), 'big': (900, 1200)}


class Support(models.Model):
    externalId = models.CharField(max_length=64)
    slug = models.SlugField(default='xxx', unique=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    unit_price = models.FloatField(default=0.0, verbose_name='Unit Price')
    vendor_price = models.FloatField(default=0.0, verbose_name='Vendor Price')
    vendor = models.ForeignKey(Vendor)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_cheapest():
        return Support.objects.order_by('unit_price').first()

    @staticmethod
    def get_available():
        support_ids = Stock.objects.exclude(stock=0).values('support').distinct()
        return Support.objects.filter(id__in=[item['support'] for item in support_ids]).order_by('unit_price')

    def get_stock(self):
        all_stock = self.stock_set.exclude(stock=0).all()
        res = {}
        for stk_item in all_stock:
            if stk_item.colour not in res:
                res[stk_item.colour] = []
            res[stk_item.colour].append({
                'size': stk_item.size,
                'stock': stk_item.stock
            })
        return res

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Support.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()

    class Meta:
        verbose_name = 'Print Support'


class Stock(models.Model):
    support = models.ForeignKey(Support)
    size = models.ForeignKey(Size)
    colour = models.ForeignKey(Colour)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return '{} - {}'.format(self.colour, self.size)

    def get_images(self):
        from gallery.models import SupportImage
        return SupportImage.objects.filter(support=self.support).all()


@receiver(pre_save, sender=Art)
@receiver(pre_save, sender=Support)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance._get_unique_slug()


@receiver(post_save, sender=Art)
def save_thumbnail(sender, **kwargs):
    filename, extension = os.path.splitext(kwargs['instance'].get_image_path())
    for k, size in Art.ThumbProperties.thumb_sizes.items():
        img = PIL_Image.open(kwargs['instance'].get_image_path())
        img.thumbnail(size)
        img.save(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)


@receiver(post_delete, sender=Art)
def clean_thumbnails(**kwargs):
    filename, extension = os.path.splitext(kwargs['file'].path)
    for k, size in Art.ThumbProperties.thumb_sizes.items():
        try:
            os.remove(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)
        except FileNotFoundError:
            pass
