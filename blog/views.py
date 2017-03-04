#!/usr/bin/env python
#coding=utf-8

import os
import markdown2
from datetime import *
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.contrib import auth
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from blog.models import Article, Attachment, Category, Tag, UserProfile
from .models import BlogComment, AppSettings
from .forms import CustomeLoginForm, BlogCommentForm, ArticleEditForm
from django.http import StreamingHttpResponse, HttpResponse, request


class About(ListView):
    template_name = 'blog/about.html'

    def get_queryset(self):
        settings = AppSettings.objects.all()
        return settings

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['settings'] = AppSettings.objects.all()
        return super(About, self).get_context_data(**kwargs)


# Create your views here.
class IndexView(ListView):
    template_name = "blog/index_summary.html"
    context_object_name = "article_list"

    def get_queryset(self):
        settings = AppSettings.objects.all()
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Article.objects.filter(status='p')\
            .values('tag__id', 'tag__name','created_time').order_by('created_time')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        kwargs['settings'] = AppSettings.objects.all()
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryView(ListView):
    template_name = "blog/index_summary.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['WebSiteName'] = AppSettings.objects.filter(name='WebSiteName')
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Article.objects.filter(category=self.kwargs['cate_id'], status='p')\
            .values('tag__id', 'tag__name','created_time').order_by('created_time')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    template_name = "blog/index_summary.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        #???
        kwargs['settings'] = AppSettings.objects.all()
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['tag_list'] = Tag.objects.filter(id=self.kwargs['tag_id']).order_by('name')
        return super(TagView, self).get_context_data(**kwargs)


class ArchiveView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(ArchiveView, self).get_context_data(**kwargs)


class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })


class AdminEditArticalView(FormView):
    form_class = ArticleEditForm
    template_name = 'admin/editArticle.html'
    context_object_name = "article"
    def get_queryset(self):
        id = int(self.kwargs['article_id'])
        article = Article.objects.get(id=id)
        article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article
    pass

