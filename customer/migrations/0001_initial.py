# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionId', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128)),
            ],
        ),
    ]
