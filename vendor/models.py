from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Vendor'
