# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from vendor.models import Vendor
from artist.models import Artist

from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'


class Art(models.Model):
    externalId = models.CharField(max_length=64)
    slug = models.SlugField(default='xxx', unique=True)
    name = models.CharField(max_length=64)
    big_image = models.ImageField(upload_to='art_big/', blank=True)
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

    class Meta:
        verbose_name = 'Art'


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


class Size(models.Model):
    name = models.CharField(max_length=254)
    stock = models.IntegerField()
    support = models.ForeignKey(Support)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Print Support Size'

@receiver(pre_save, sender=Art)
@receiver(pre_save, sender=Support)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = instance._get_unique_slug()
