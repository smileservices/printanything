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
    return "art/{0}/{1}.{2}".format(instance.product.id, get_random_string(24),
                                    filename.split(".")[-1].lower())  # todo finish the save path


class Image(models.Model):
    relative_path = models.ImageField(upload_to=get_save_path)
    product = models.ForeignKey(Art, on_delete=models.CASCADE, related_name='images')

    def get_image_absolute_url(self):
        return os.path.join(settings.BASE_DIR, self.relative_path.url)

    def get_thumb_absolute_url(self, size):
        filename, extension = os.path.splitext(self.relative_path)
        thumb_name = filename + "_thumb_{0}".format("_".join(map(str, size))) + extension
        return os.path.join(settings.BASE_DIR, thumb_name)


@receiver(post_save, sender=Image)
def save_thumbnail(sender, **kwargs):
    sizes = [(120, 120), ]
    filename, extension = os.path.splitext(kwargs['instance'].relative_path.url)
    for size in sizes:
        img = PIL_Image.open(kwargs['instance'].get_image_absolute_url())
        img.thumbnail(size)
        img.save(filename + "_thumb_{0}".format("_".join(map(str, size))) + extension)
