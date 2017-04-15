#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'comment',)
    search_fields = ('name',)

class WebSiteAboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'comment',)
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display',)
    search_fields = ('name',)

class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('job_title', )
    search_fields = ('job_title',)

class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('job_title', )
    search_fields = ('job_title',)

class WebSiteLevelAdmin(admin.ModelAdmin):
    list_display = ('levels', 'description',)
    search_fields = ('levels',)