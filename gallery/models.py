import os
from django.db import models
from PIL import Image as PIL_Image
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from product.models import Art


# Create your models here.

def get_save_path(instance, filename):
    return "art/{0}/{1}.{2}".format(
        instance.art.id,
        get_random_string(24),
        filename.split(".")[-1].lower()
    )


def get_thumb_url(instance, size):
    filename, extension = os.path.splitext(instance.relative_path.url)
    thumb_name = filename + "_thumb_{0}".format("_".join(map(str, size))) + extension
    return thumb_name


class Image(models.Model):
    relative_path = models.ImageField(upload_to=get_save_path)
    art = models.ForeignKey(Art, on_delete=models.CASCADE, related_name='images', db_constraint=False)
    primary = models.BooleanField()

    def get_image_path(self):
        return os.path.join(settings.BASE_DIR, self.relative_path.url[1:])

    def get_image_url(self):
        return self.relative_path.url

    def get_thumb_big_url(self):
        return get_thumb_url(self, (800, 1128))

    def get_thumb_med_url(self):
        return get_thumb_url(self, (600, 900))

    def get_thumb_small_url(self):
        return get_thumb_url(self, (600, 682))

    #todo implement delete


@receiver(post_save, sender=Image)
def save_thumbnail(sender, **kwargs):
    sizes = [(600, 900), (600, 682), (800, 1128)]
    filename, extension = os.path.splitext(kwargs['instance'].get_image_path())
    for size in sizes:
        img = PIL_Image.open(kwargs['instance'].get_image_path())
        img.thumbnail(size)
        img.save(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)
