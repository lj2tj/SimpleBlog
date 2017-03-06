#!/usr/bin/env python
#coding=utf-8

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog.models import UserProfile, BlogComment, AppSettings
from django.http import StreamingHttpResponse, HttpResponse


WebSiteName = AppSettings.objects.filter(name='WebSiteName')[0].value

def ValidateUserName(request):
    """
    Validate if an user already exists, when registering a new user, if the user name already exists,
    return alert message, if it is a new user, retuan 1.
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

def RegisterPage(request):
    """
    Show user register page.
    """
    return render_to_response("user/userregister.html", RequestContext(request, {"WebSiteName" : WebSiteName}))


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
        return HttpResponseRedirect("/usercenter")

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
            if UserProfile.objects.filter(username=username):
                errors.append("该用户名已存在!")
                return render_to_response("/", \
                   RequestContext(request, {'memUserId': username, 'errors': errors}))
            user = UserProfile()
            user.username = username
            user.password = password1
            user.save()

        return render_to_response("/")

    except Exception, e:
        errors.append(str(e))
        return render_to_response("user/userregister.html", 
            RequestContext(request, {'memUserId': '', 'errors': errors}))


def LoginPage(request):
    return render_to_response("user/login.html", RequestContext(request, {"WebSiteName" : WebSiteName}))


def login(request):
    """
    Customer login.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("/usercenter")
    else:
        if request.method == 'POST':
            username = request.POST.get('name', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/usercenter")

        return render_to_response("user/login.html", RequestContext(request, {'curtime': datetime.now()}))


def UserCenter(request):
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request))

    return render_to_response("user/usercenter.html", RequestContext(request))


def Purchase(request):
    """
    By a document.
    """
    article_id = '-1'
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", RequestContext(request, {'purchase':True, 'article_id': article_id}))
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


def file_iterator(file_name, chunk_size=512):
    """File downloader"""
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break