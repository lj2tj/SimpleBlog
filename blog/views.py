#!/usr/bin/env python
#coding=utf-8

from datetime import *
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.http import request, response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog.models import Article, Attachment, Category, Tag
import markdown2
from .models import BlogComment, AppSettings
from .forms import BlogCommentForm, ArticleEditForm



'''
def global_setting(request):
    existing_settings = AppSettings.objects.all()
    if(existing_settings.count() > 0):
        return existing_settings.first()
    pass
'''
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
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 第五周新增
    def get_context_data(self, **kwargs):
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
        kwargs['category_list'] = Category.objects.all().order_by('created_time')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
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

''''
def userRegister(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
    if request.user.is_authenticated():  # a*******************
        return HttpResponseRedirect("/user")
    try:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password1 = request.POST.get('password', '')
            errors = []

            registerForm = RegisterForm({'username': username, 'password1': password1, 'password2': password2,
                                         'email': email})  # b********
            if not registerForm.is_valid():
                errors.extend(registerForm.errors.values())
                return render_to_response("user/register.html", RequestContext(request, {'curtime': curtime,
                                                                                             'username': username,
                                                                                             'email': email,
                                                                                             'errors': errors}))
            if password1 != password2:
                errors.append("两次输入的密码不一致!")
                return render_to_response("blog/userregister.html", RequestContext(request, {'curtime': curtime,
                                                                                             'username': username,
                                                                                             'email': email,
                                                                                             'errors': errors}))

            filterResult = User.objects.filter(username=username)  # c************
            if len(filterResult) > 0:
                errors.append("用户名已存在")
                return render_to_response("blog/userregister.html", RequestContext(request, {'curtime': curtime,
                                                                                             'username': username,
                                                                                             'email': email,
                                                                                             'errors': errors}))

            user = User()  # d************************
            user.username = username
            user.set_password(password1)
            user.email = email
            user.save()
            # 用户扩展信息 profile
            profile = UserProfile()  # e*************************
            profile.user_id = user.id
            profile.phone = phone
            profile.save()
            # 登录前需要先验证
            newUser = auth.authenticate(username=username, password=password1)  # f***************
            if newUser is not None:
                auth.login(request, newUser)  # g*******************
                return HttpResponseRedirect("/user")
    except Exception, e:
        errors.append(str(e))
        return render_to_response("blog/userregister.html", RequestContext(request, {'curtime': curtime,
                                                                                     'username': username,
                                                                                     'email': email,
                                                                                     'errors': errors}))

    return render_to_response("blog/userregister.html", RequestContext(request, {'curtime': curtime}))
'''