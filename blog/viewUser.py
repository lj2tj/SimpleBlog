#!/usr/bin/env python
#coding=utf-8

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.contrib import auth
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from blog.models import UserProfile
from .models import BlogComment, AppSettings
from .forms import CustomeLoginForm, BlogCommentForm, ArticleEditForm
from django.http import StreamingHttpResponse, HttpResponse, request



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