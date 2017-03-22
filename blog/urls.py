#!/usr/bin/env python
#coding=utf-8

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from blog import views, viewUser

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?i)article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^(?i)category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^(?i)tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^(?i)archive/(?P<year>\d+)/(?P<month>\d+)$', views.ArchiveView.as_view(), name='archive'),
    url(r'^(?i)article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), \
    name='comment'),
    url(r'^(?i)about$', views.About.as_view(), name='about'),
    url(r'^(?i)usercenter$', login_required(viewUser.UserCenter), name='usercenter'),
    url(r'^(?i)UpdateUserInfo$', viewUser.UpdateUserInfo, name='UpdateUserInfo'),
    url(r'^(?i)ValidateUserName$', viewUser.ValidateUserName, name='ValidateUserName'),
    url(r'^(?i)RegisterPage$', viewUser.registerPage, name='RegisterPage'),
    url(r'^(?i)register$', viewUser.register, name='register'),
    url(r'^(?i)login$', viewUser.login, name='login'),
    url(r'^(?i)logout$', viewUser.logout, name='logout'),
    url(r'^(?i)loginpage$', viewUser.loginPage, name='LoginPage'),
    url(r'^(?i)purchase/(?P<attachment_id>\d+)$', login_required(viewUser.Purchase), \
    name='purchase'),
]
