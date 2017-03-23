#!/usr/bin/env python
#coding=utf-8

import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, render_to_response
from django.template import RequestContext, loader
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from blog.models import UserProfile, UserDownloadFile, BlogComment, AppSettings
from blog.models import Article, Attachment, Category, Tag, UserProfile
from django.http import StreamingHttpResponse, HttpResponse

WebSiteName = ''
if AppSettings.objects.filter(name='WebSiteName') is not None:
    WebSiteName = AppSettings.objects.filter(name='WebSiteName')[0].value

def UpdateUserInfo(request):
    """
    Update user info.
    """
    try:
        if not request.user.is_authenticated():
            return render_to_response("user/login.html", \
            RequestContext(request, {"WebSiteName" : WebSiteName}))

        user = User.objects.filter(id=request.user.id)[0]
        #user = User(username=current_user.username, password=current_user.password)
        email = request.GET.get('email', '')

        if email.find("@") <= 0:
            return HttpResponse("邮箱地址不正确")
        else:
            print user.last_login
            user.email = email
            user.save()
        return HttpResponse("1")
    except Exception, e:
        return HttpResponse(e)

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

    category_list = Category.objects.all().order_by('created_time')
    uploaded_files = Article.objects.filter(user_id=base_info.id)
    if not any(uploaded_files):
        uploaded_files = []

    downloaded_files = UserDownloadFile.objects.filter(user_id=base_info.id)
    if not any(downloaded_files):
        downloaded_files = []

    dic = {'category_list':category_list, \
    'base_info': base_info, 'uploaded_files': uploaded_files, \
    'downloaded_files': downloaded_files}
    return render(request, "user/usercenter.html", dic)


def Purchase(request, attachment_id):
    """
    By a document.
    """
    if not request.user.is_authenticated():
        return render_to_response("user/login.html", \
            RequestContext(request, {'purchase':True, 'attachment_id': attachment_id}))

    if attachment_id == -1:
        return HttpResponse('No such file.')

    upload_file_path = settings.MEDIA_ROOT

    if upload_file_path is None:
        return HttpResponse('System setting error, upload_file_path is empty.')

    the_file = Attachment.objects.filter(id=attachment_id)
    if the_file is None:
        return HttpResponse('No such file.')

    file_full_name = os.path.join(upload_file_path, unicode(the_file[0].attachment))
    print 'file_full_name', file_full_name
    response = StreamingHttpResponse(file_iterator(file_full_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file[0].name)
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
