# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-07 22:16
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20170106_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
    ]
