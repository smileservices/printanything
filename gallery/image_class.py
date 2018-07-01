import os
from django.db import models
from django.conf import settings


class Image:
    relative_path = {'url': ''}
    thumb_sizes = {'med': (600, 900), 'small': (600, 682), 'big': (800, 1128)}

    def get_image_path(self):
        return os.path.join(settings.BASE_DIR, self.relative_path.url[1:])

    def get_image_url(self):
        return self.relative_path.url

    def get_thumb_big_url(self):
        return get_thumb_url(self, self.thumb_sizes['big'])

    def get_thumb_med_url(self):
        return get_thumb_url(self, self.thumb_sizes['med'])

    def get_thumb_small_url(self):
        return get_thumb_url(self, self.thumb_sizes['small'])


def get_thumb_url(instance, size):
    filename, extension = os.path.splitext(instance.relative_path.url)
    thumb_name = filename + "_thumb_{0}".format("_".join(map(str, size))) + extension
    return thumb_name
