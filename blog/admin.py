#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Tag, Attachment, AppSettings, SettingsAdmin

admin.site.register(Article)
admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(AppSettings, SettingsAdmin)
