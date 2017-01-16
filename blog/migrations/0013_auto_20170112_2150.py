# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('blog', '0012_auto_20170110_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo', models.ImageField(height_field=120, upload_to=b'', width_field=100, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('mobile_phone', models.CharField(max_length=20, null=True, verbose_name=b'\xe7\xa7\xbb\xe5\x8a\xa8\xe7\x94\xb5\xe8\xaf\x9d')),
                ('location', models.CharField(max_length=200, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'verbose_name': '\u8ba4\u8bc1\u4f5c\u8005',
                'verbose_name_plural': '\u8ba4\u8bc1\u4f5c\u8005',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=20, verbose_name=b'\xe8\x81\x8c\xe5\x8a\xa1')),
            ],
            options={
                'verbose_name': '\u804c\u52a1',
                'verbose_name_plural': '\u804c\u52a1',
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=20, verbose_name=b'\xe8\x81\x8c\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u804c\u79f0',
                'verbose_name_plural': '\u804c\u79f0',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.OneToOneField(null=True, blank=True, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='author',
            name='job_title',
            field=models.ForeignKey(to='blog.JobTitle', null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='position',
            field=models.ForeignKey(to='blog.JobPosition', null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
