#!/usr/bin/env python
#coding=utf-8

from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Tag, Attachment, AppSettings

admin.site.register(Article)
admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(AppSettings)

'''
class ArticleCreationForm(Article):  # 编辑用户表单重新定义，继承自UserChangeForm
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['body'].required = True
        self.fields['abstract'].required = True

class ArticleChangeForm(Article):  # 编辑用户表单重新定义，继承自UserChangeForm
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['body'].required = True
        self.fields['abstract'].required = True

class CustomArticle(Article):
	def __init__(self, *args, **kwargs):
		super(CustomArticle, self).__init__(*args, **kwargs)
		self.list_display = ('title', 'body', 'abstract')
		self.search_fields = ('title', 'body', 'abstract')
		self.form = ArticleChangeForm
		self.add_form = ArticleCreationForm
		pass

admin.site.register(Article, CustomArticle)
'''