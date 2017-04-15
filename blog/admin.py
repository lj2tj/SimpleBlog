#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Tag, Attachment, AppSettings, JobPosition, JobTitle, WebSiteLevel, WebSiteAbout
from blog.modelAdmin import CategoryAdmin, SettingsAdmin, WebSiteAboutAdmin

admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(AppSettings, SettingsAdmin)
admin.site.register(JobPosition)
admin.site.register(JobTitle)
admin.site.register(WebSiteLevel)
admin.site.register(WebSiteAbout, WebSiteAboutAdmin)