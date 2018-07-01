from __future__ import unicode_literals
import os
from django.db import models
from PIL import Image as PIL_Image
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from product.models import Art, Support, Colour
from django_cleanup.signals import cleanup_pre_delete
from gallery.image_class import Image


# Create your models here.

def get_art_save_path(instance, filename):
    return "art/{0}/{1}.{2}".format(
        instance.art.id,
        get_random_string(24),
        filename.split(".")[-1].lower()
    )


def get_support_save_path(instance, filename):
    return "support/{0}/{1}/{2}.{3}".format(
        instance.support.id,
        instance.colour.id,
        get_random_string(24),
        filename.split(".")[-1].lower()
    )


class ArtImage(Image, models.Model):
    relative_path = models.ImageField(upload_to=get_art_save_path)
    art = models.ForeignKey(Art, on_delete=models.CASCADE, related_name='images', db_constraint=False)
    primary = models.BooleanField()


class SupportImage(Image, models.Model):
    relative_path = models.ImageField(upload_to=get_support_save_path)
    support = models.ForeignKey(Support, on_delete=models.CASCADE, related_name='images', db_constraint=False)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, related_name='images', db_constraint=False)
    primary = models.BooleanField()


# @receiver(cleanup_post_delete, sender=Image)
def clean_thumbnails(**kwargs):
    filename, extension = os.path.splitext(kwargs['file'].path)
    for k, size in ArtImage.thumb_sizes.items():
        try:
            os.remove(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)
        except FileNotFoundError:
            pass


cleanup_pre_delete.connect(clean_thumbnails)


@receiver(post_save, sender=SupportImage)
@receiver(post_save, sender=ArtImage)
def save_thumbnail(sender, **kwargs):
    filename, extension = os.path.splitext(kwargs['instance'].get_image_path())
    for k, size in ArtImage.thumb_sizes.items():
        img = PIL_Image.open(kwargs['instance'].get_image_path())
        img.thumbnail(size)
        img.save(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)
