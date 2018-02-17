# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Customer(models.Model):
    email = models.CharField(max_length=64)

    def __str__(self):
        return self.email
