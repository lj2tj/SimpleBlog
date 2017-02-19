#!/usr/bin/env python
#coding=utf-8

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from blog import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^about$', views.About.as_view(), name='about'),
    url(r'^user/usercenter$',login_required(views.UserCenter), name='usercenter'),
    url(r'^RegisterPage$', views.RegisterPage, name='RegisterPage'),
    url(r'^register$', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^LoginPage/', views.LoginPage, name='LoginPage'),
    url(r'^purchase/(?P<article_id>\d+)$', login_required(views.Purchase), name='purchase'),
]
