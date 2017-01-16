# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170110_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.TextField(help_text=b'\xe5\x8f\xaf\xe9\x80\x89\xef\xbc\x8c\xe5\xa6\x82\xe8\x8b\xa5\xe4\xb8\xba\xe7\xa9\xba\xe5\xb0\x86\xe6\x91\x98\xe5\x8f\x96\xe6\xad\xa3\xe6\x96\x87\xe7\x9a\x84\xe5\x89\x8d1000\xe4\xb8\xaa\xe5\xad\x97\xe7\xac\xa6', max_length=1000, null=True, verbose_name=b'\xe6\x91\x98\xe8\xa6\x81', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='en_keywords',
            field=models.CharField(help_text=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe4\xb9\x8b\xe9\x97\xb4\xe4\xbb\xa5\xe8\x8b\xb1\xe6\x96\x87\xe9\x80\x97\xe5\x8f\xb7\xef\xbc\x88,\xef\xbc\x89\xe5\x88\x86\xe9\x9a\x94', max_length=100, verbose_name=b'Key Words', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='keywords',
            field=models.CharField(help_text=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe4\xb9\x8b\xe9\x97\xb4\xe4\xbb\xa5\xe9\x80\x97\xe5\x8f\xb7\xef\xbc\x88,\xef\xbc\x89\xe5\x88\x86\xe9\x9a\x94', max_length=100, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97', blank=True),
        ),
    ]
