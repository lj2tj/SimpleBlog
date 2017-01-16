# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0016_remove_article_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(height_field=120, upload_to=b'', width_field=100, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('mobile_phone', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xa7\xbb\xe5\x8a\xa8\xe7\x94\xb5\xe8\xaf\x9d')),
                ('location', models.CharField(max_length=200, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('job_title', models.ForeignKey(to='blog.JobTitle', null=True)),
                ('position', models.ForeignKey(to='blog.JobPosition', null=True)),
                ('user', models.OneToOneField(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u8ba4\u8bc1\u4f5c\u8005',
                'verbose_name_plural': '\u8ba4\u8bc1\u4f5c\u8005',
            },
        ),
        migrations.RemoveField(
            model_name='author',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='author',
            name='job_title',
        ),
        migrations.RemoveField(
            model_name='author',
            name='position',
        ),
        migrations.RemoveField(
            model_name='author',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='blog.UserProfile'),
        ),
    ]
