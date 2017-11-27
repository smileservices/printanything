# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Customer(models.Model):
    sessionId = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
