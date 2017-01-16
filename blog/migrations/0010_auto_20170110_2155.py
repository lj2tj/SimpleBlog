# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170107_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_name', models.CharField(max_length=20, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99\xe6\x98\xbe\xe7\xa4\xba\xe5\x90\x8d')),
                ('application_copyright', models.CharField(max_length=200, verbose_name=b'\xe7\x89\x88\xe6\x9d\x83')),
                ('register_info', models.CharField(max_length=100, verbose_name=b'\xe5\xa4\x87\xe6\xa1\x88\xe4\xbf\xa1\xe6\x81\xaf')),
                ('telphone1', models.CharField(max_length=100, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe7\x94\xb5\xe8\xaf\x9d1')),
                ('telphone2', models.CharField(max_length=100, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe7\x94\xb5\xe8\xaf\x9d2')),
                ('telphone3', models.CharField(max_length=100, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe7\x94\xb5\xe8\xaf\x9d3')),
                ('email', models.EmailField(max_length=100, verbose_name=b'\xe7\x94\xb5\xe5\xad\x90\xe9\x82\xae\xe4\xbb\xb6')),
                ('small_logo', models.ImageField(height_field=40, width_field=80, upload_to=b'', help_text=models.CharField(max_length=20, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99\xe6\x98\xbe\xe7\xa4\xba\xe5\x90\x8d'), verbose_name=b'\xe5\xb0\x8f\xe5\x9b\xbe\xe6\xa0\x87')),
                ('medium_logo', models.ImageField(height_field=80, width_field=200, upload_to=b'', help_text=models.CharField(max_length=20, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99\xe6\x98\xbe\xe7\xa4\xba\xe5\x90\x8d'), verbose_name=b'\xe4\xb8\xad\xe5\x9b\xbe\xe6\xa0\x87')),
                ('big_logo', models.ImageField(height_field=200, width_field=400, upload_to=b'', help_text=models.CharField(max_length=20, verbose_name=b'\xe7\xbd\x91\xe7\xab\x99\xe6\x98\xbe\xe7\xa4\xba\xe5\x90\x8d'), verbose_name=b'\xe5\xa4\xa7\xe5\x9b\xbe\xe6\xa0\x87')),
            ],
            options={
                'verbose_name': '\u7f51\u7ad9\u914d\u7f6e',
                'verbose_name_plural': '\u7f51\u7ad9\u914d\u7f6e',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='path',
            field=models.FileField(upload_to=b'D:\\Code\\Python\\Blog\\django-blog-tutorial-master\\UploadFolder', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.CharField(help_text=b'\xe5\x8f\xaf\xe9\x80\x89\xef\xbc\x8c\xe5\xa6\x82\xe8\x8b\xa5\xe4\xb8\xba\xe7\xa9\xba\xe5\xb0\x86\xe6\x91\x98\xe5\x8f\x96\xe6\xad\xa3\xe6\x96\x87\xe7\x9a\x84\xe5\x89\x8d1000\xe4\xb8\xaa\xe5\xad\x97\xe7\xac\xa6', max_length=1000, null=True, verbose_name=b'\xe6\x91\x98\xe8\xa6\x81', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6', to='blog.Attachment', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=tinymce.models.HTMLField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', to='blog.Category', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='en_keywords',
            field=models.CharField(help_text=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe4\xb9\x8b\xe9\x97\xb4\xe4\xbb\xa5\xe8\x8b\xb1\xe6\x96\x87\xe9\x80\x97\xe5\x8f\xb7\xef\xbc\x88,\xef\xbc\x89\xe5\x88\x86\xe9\x9a\x94', max_length=100, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='keywords',
            field=models.CharField(help_text=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe4\xb9\x8b\xe9\x97\xb4\xe4\xbb\xa5\xe9\x80\x97\xe5\x8f\xb7\xef\xbc\x88\xef\xbc\x8c\xef\xbc\x89\xe5\x88\x86\xe9\x9a\x94', max_length=100, verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_modified_time',
            field=models.DateTimeField(verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='article',
            name='price',
            field=models.DecimalField(default=1, help_text=b'\xe6\x96\x87\xe6\xa1\xa3\xe4\xbb\xb7\xe6\xa0\xbc\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe5\x85\x83', verbose_name=b'\xe4\xbb\xb7\xe6\xa0\xbc', max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(max_length=1, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x8a\xb6\xe6\x80\x81', choices=[(b'd', b'Draft'), (b'p', b'Published')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe9\x9b\x86\xe5\x90\x88', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=70, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98'),
        ),
        migrations.AlterField(
            model_name='article',
            name='topped',
            field=models.BooleanField(default=False, verbose_name=b'\xe7\xbd\xae\xe9\xa1\xb6'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe9\x87\x8f'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='download_times',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe4\xb8\x8b\xe8\xbd\xbd\xe6\xac\xa1\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='name',
            field=models.CharField(max_length=120, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8a\xe4\xbc\xa0\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='article',
            field=models.ForeignKey(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x89\x80\xe5\xb1\x9e\xe6\x96\x87\xe7\xab\xa0', to='blog.Article'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='body',
            field=tinymce.models.HTMLField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x86\x85\xe5\xae\xb9'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='user_email',
            field=models.EmailField(max_length=255, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe8\x80\x85\xe9\x82\xae\xe7\xae\xb1'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='user_name',
            field=models.CharField(max_length=100, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe8\x80\x85\xe5\x90\x8d\xe5\xad\x97'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'\xe7\xb1\xbb\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe5\x90\x8d'),
        ),
    ]
