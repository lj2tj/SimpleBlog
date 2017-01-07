# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-06 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170106_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.AddField(
            model_name='article',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, help_text='文档价格，单位：元', max_digits=6, verbose_name='价格'),
        ),
    ]