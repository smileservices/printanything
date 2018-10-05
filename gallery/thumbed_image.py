import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from PIL import Image as PIL_Image

"""

Maybe we can use this one to replace the Image class usage

"""


class ThumbedModel():

    def get_thumb_url(self, size):
        filename, extension = os.path.splitext(getattr(self, self.ThumbProperties.image_field_name).url)
        thumb_name = filename + "_thumb_{0}".format("_".join(map(str, self.ThumbProperties.thumb_sizes[size])) + extension)
        return thumb_name

    def __getattr__(self, item):
        if item[:9] == 'get_thumb':
            return getattr(self, 'get_thumb_url')(item[10:])
        raise AttributeError()

    class ThumbProperties:
        image_field_name = 'relative_path'
        thumb_sizes = {'small': (300, 600), 'med': (600, 900), 'big': (900, 1200)}
