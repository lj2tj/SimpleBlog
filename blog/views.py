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

    # 第五周新增
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
        kwargs['settings'] = AppSettings.objects.all()
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


# 第五周新增
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


def ValidateUserName(request):
    name = request.GET.get('name','')
    if name == '':
        return HttpResponse("Empty user name error!")
    else:
        user = User.objects.filter(username=name)
        print(user)
        if user is None or user.__len__() == 0:
            return HttpResponse('1')
        else:
            return HttpResponse('User [%s] already exists' % name)

def RegisterPage(request):
    return render_to_response("user/userregister.html", RequestContext(request))


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/user/usercenter")

    errors = []
    try:
        if request.method == 'POST':
            username = request.POST.get('memUserId', '')
            password1 = request.POST.get('memPassword', '')
            password_confirm = request.POST.get('password_confirm', '')

            if password1 != password_confirm:
                errors.append("两次输入的密码不一致!")
                return render_to_response("/", RequestContext(request, {'memUserId': username,
                                                                               'errors': errors}))
            if UserProfile.objects.filter(username=username):
                errors.append("该用户名已存在!")
                return render_to_response("/", RequestContext(request, {'memUserId': username,
                                                                        'errors': errors}))
            user = UserProfile()
            user.username = username
            user.password = password1
            user.save()

        return render_to_response("/")

    except Exception, e:
        errors.append(str(e))
        return render_to_response("user/userregister.html", RequestContext(request, {'memUserId': '',
                                                                                     'errors': errors}))


def LoginPage(request):
    return render_to_response("user/login.html", RequestContext(request))


def login(request):
    """
    Customer login.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("/user/usercenter" )
    else:
        if request.method == 'POST':
            print("POST")
            username = request.POST.get('name', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/user/usercenter")

        return render_to_response("user/login.html", RequestContext(request, {'curtime': datetime.now()}))


class UserCenter(DetailView):
    model = UserProfile
    template_name = "user/usercenter.html"

    def get_object(self, queryset=None):
        obj = super(UserCenter, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
        kwargs['settings'] = AppSettings.objects.all()
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        return super(UserCenter, self).get_context_data(**kwargs)


def Purchase(request):
    """
    By a document.
    """
    print("====================================")
    article_id = 'article_id'
    print('article_id: ', article_id)
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request, {'purchase':True, 'article_id': article_id}))
    else:
        if request.method == 'GET':
            print(request.user)

    the_file_name = Article.objects.filter(id=article_id)
    print(the_file_name)
    if the_file_name == None:
        """TODO : Could not find the file"""
        return None
    UploadFilePath = AppSettings.objects.filter(name='UploadFilePath')
    response = StreamingHttpResponse(file_iterator(os.path.join(UploadFilePath, the_file_name)))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response


def file_iterator(file_name, chunk_size=512):
    """File downloader"""
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break