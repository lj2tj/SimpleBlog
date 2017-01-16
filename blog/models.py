#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from collections import defaultdict
from blog_project import settings
from tinymce.models import HTMLField

import datetime

class JobPosition(models.Model):
    job_title = models.CharField('职务', max_length=20)

    class Meta:
        verbose_name = "职务"
        verbose_name_plural = verbose_name

class JobTitle(models.Model):
    job_title = models.CharField('职称', max_length=20)

    class Meta:
        verbose_name = "职称"
        verbose_name_plural = verbose_name

class Location(models.Model):
    country = ('中国', '其它',)
    provence = ('北京','天津','上海','重庆',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=('用户'))
    photo = models.ImageField("头像", width_field=100, height_field=120, null=True)
    mobile_phone = models.CharField('移动电话', max_length=20, null=True)
    position = models.ForeignKey('JobPosition', null=True)
    job_title = models.ForeignKey('JobTitle', null=True)
    location = models.CharField('地址', max_length=200, null=True)

    class Meta:
        verbose_name = "认证作者"
        verbose_name_plural = verbose_name


# Create your models here.
class ArticleManage(models.Manager):
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)  # 模板不支持defaultdict


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    objects = ArticleManage()

    title = models.CharField('标题', max_length=70)
    body = HTMLField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.TextField('摘要', max_length=1000, blank=True, null=True, help_text="可选，如若为空将摘取正文的前1000个字符")
    keywords = models.CharField("关键字", max_length=100, blank=True, help_text="关键字之间以逗号（,）分隔")
    en_keywords = models.CharField("Key Words", max_length=100, blank=True, help_text="关键字之间以英文逗号（,）分隔")
    views = models.PositiveIntegerField('浏览量', default=0, editable=False)
    likes = models.PositiveIntegerField('点赞数', default=0, editable=False)
    topped = models.BooleanField('置顶', default=False)
    price = models.DecimalField('价格', default=1, blank=False, decimal_places=2, max_digits=6, help_text="文档价格，单位：元")
    attachment = models.ForeignKey('Attachment', verbose_name='附件', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    user = models.OneToOneField('UserProfile', editable=False, null=True, blank=True)
    #user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

    # 第五周：新增 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk}) 

class Attachment(models.Model):
    """文章附件"""
    name = models.CharField('附件名', max_length=120)
    path = models.FileField(upload_to=settings.UPLOAD_PATH, blank=True)
    upload_time = models.DateTimeField('上传时间', auto_now_add=True)
    download_times = models.PositiveIntegerField('下载次数', default=0, editable=False)

    class Meta:
        verbose_name = "附件"
        verbose_name_plural = verbose_name

        
class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


# # 第五周：新增评论
class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = HTMLField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]


class AppSettings(models.Model):
    """
    网站基本配置信息
    """
    application_name = models.CharField('网站显示名', max_length=20, blank=False )
    application_copyright = models.CharField('版权', max_length=200)
    register_info = models.CharField('备案信息', max_length=100)
    telphone1 = models.CharField('联系电话1', max_length=100)
    telphone2 = models.CharField('联系电话2', max_length=100)
    telphone3 = models.CharField('联系电话3', max_length=100)
    email = models.EmailField('电子邮件', max_length=100)
    small_logo = models.ImageField('小图标', width_field=80, height_field=40, help_text=application_name)
    medium_logo = models.ImageField('中图标', width_field=200, height_field=80, help_text=application_name)
    big_logo = models.ImageField('大图标', width_field=400, height_field=200, help_text=application_name)

    class Meta:
        verbose_name = "网站配置"
        verbose_name_plural = verbose_name
    pass