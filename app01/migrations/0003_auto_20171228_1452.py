# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-12-28 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20171227_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_id',
            field=models.CharField(max_length=100, verbose_name='ID'),
        ),
    ]
