# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_remove_article_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.OneToOneField(default=-1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
