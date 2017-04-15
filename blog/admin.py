#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Tag, Attachment, AppSettings, JobPosition, JobTitle, WebSiteLevel, WebSiteAbout
from blog.modelAdmin import CategoryAdmin, SettingsAdmin, WebSiteAboutAdmin, JobPositionAdmin, JobTitleAdmin, WebSiteLevelAdmin

admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(AppSettings, SettingsAdmin)
admin.site.register(JobPosition, JobPositionAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(WebSiteLevel, WebSiteLevelAdmin)
admin.site.register(WebSiteAbout, WebSiteAboutAdmin)