#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog.models import UserProfile, BlogComment, AppSettings
from blog.models import Article, Attachment, Category, Tag, UserProfile
from django.http import StreamingHttpResponse, HttpResponse


WebSiteName = AppSettings.objects.filter(name='WebSiteName')[0].value

def UpdateUserInfo(request):
    """
    Update user info.
    """
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", \
        RequestContext(request, {"WebSiteName" : WebSiteName}))

    user_id = request.user.id
    user = User.objects.filter(id=user_id)
    email = request.POST.get('email', '')
    if email.find("@") <= 0:
        return HttpResponse("邮箱地址不正确")
    else:
        user.email = email
        user.save()
        return HttpResponse("1")

def ValidateUserName(request):
    """
    Validate if an user already exists when registering a new user,
    if yes return alert message, else retuan 1.
    """
    name = request.GET.get('name', '')
    if name == '':
        return HttpResponse("Empty user name error!")
    else:
        user = User.objects.filter(username=name)
        if user is None or user.__len__() == 0:
            return HttpResponse('1')
        else:
            return HttpResponse('User [%s] already exists' % name)


def registerPage(request):
    """
    Show user register page.
    """
    return render_to_response("user/userregister.html", \
        RequestContext(request, {"WebSiteName" : WebSiteName}))


def register(request):
    """
    Register a new user.
    """
    if request.user.is_authenticated():
        """
        If current user already login website, \
        don't need to register a new one, \
        go to user center directly.
        """
        return HttpResponseRedirect("usercenter")

    errors = []
    try:
        if request.method == 'POST':
            username = request.POST.get('memUserId', '')
            password1 = request.POST.get('memPassword', '')
            password_confirm = request.POST.get('password_confirm', '')
            if password1 != password_confirm:
                errors.append("两次输入的密码不一致!")
                return render_to_response("/", \
                    RequestContext(request, {'memUserId': username, 'errors': errors}))
            if User.objects.filter(username=username):
                errors.append("该用户名已存在!")
                return render_to_response("/", \
                   RequestContext(request, {'memUserId': username, 'errors': errors}))
            user = User()
            user.username = username
            user.set_password(password1)
            user.is_staff = 1
            user.save()

        user = auth.authenticate(username=username, password=password1)
        auth.login(request, user)
        return render_to_response("user/usercenter.html", RequestContext(request))

    except Exception, e:
        errors.append(str(e))
        return render_to_response("user/userregister.html", \
            RequestContext(request, {'memUserId': '', 'errors': errors}))


def loginPage(request):
    """
    User login page.
    """
    return render_to_response("user/login.html", \
        RequestContext(request, {"WebSiteName" : WebSiteName}))


def login(request):
    """
    Customer login.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("usercenter")
    else:
        if request.method == 'POST':
            username = request.POST.get('memUserId', '')
            password = request.POST.get('memPassword', '')
            print username, password
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("usercenter")

        return render_to_response("user/login.html", \
            RequestContext(request, {'curtime': datetime.now()}))


def UserCenter(request):
    """
    Website user center.
    """
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request))
    base_info = request.user
    print base_info
    category_list = Category.objects.all().order_by('created_time')
    return render_to_response("user/usercenter.html", \
    RequestContext(request, {'category_list':category_list, 'base_info': base_info}))


def Purchase(request):
    """
    By a document.
    """
    article_id = '-1'
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", \
            RequestContext(request, {'purchase':True, 'article_id': article_id}))
    else:
        if request.method == 'GET':
            article_id = request.GET.get('article_id', '-1')
        else:
            article_id = -1

    if article_id == -1:
        return HttpResponse('No such file.')

    the_file_name = Article.objects.filter(id=article_id)
    if the_file_name == None:
        """TODO : Could not find the file"""
        return HttpResponse('No such file.')

    UploadFilePath = AppSettings.objects.filter(name='UploadFilePath')
    if UploadFilePath == null:
        return HttpResponse('System setting error, UploadFilePath is empty.')

    response = StreamingHttpResponse(file_iterator(os.path.join(UploadFilePath, the_file_name)))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def logout(request):
    """
    Logout website.
    """
    auth.logout(request)
    return HttpResponseRedirect("/")



def file_iterator(file_name, chunk_size=512):
    """File downloader"""
    with open(file_name) as new_file:
        while True:
            block = new_file.read(chunk_size)
            if block:
                yield block
            else:
                break