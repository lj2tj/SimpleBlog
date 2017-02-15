#!/usr/bin/env python
#coding=utf-8

from django.conf.urls import url, include
from blog import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^about$', views.About.as_view(), name='about'),
    url(r'^user/usercenter$', views.UserCenter, name='usercenter'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
]
