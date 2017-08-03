# -*- coding: utf-8 -*-
import datetime
import logging

import simplejson as simplejson
from django.contrib.auth import logout, login, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, response
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password


# Create your views here.


def index(request):
    return render(request, 'index.html')


def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            remember_me = request.POST.get('remember_me', '0')
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    path = request.session.get('url_path', '/')
                    response = redirect(path)
                    # remember me
                    if remember_me == '1':
                        response.set_cookie('username', username,
                                            expires=datetime.datetime.now() + datetime.timedelta(days=7))
                    else:
                        response.set_cookie('username', '', max_age=-1)
                else:
                    reason = "1"
                    return render(request, 'login.html', locals())
                return response
            else:
                # To Do 非法数据越过页面校验 output server validate reason to page
                return render(request, 'login.html', locals())
        else:
            login_form = LoginForm()
    except Exception as e:
        logging.error(e)
    return render(request, 'login.html', locals())


def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logging.error(e)
    return redirect('/login')


@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册 使用django forms
                user = UserInfo.objects.create(username=reg_form.cleaned_data["username"],
                                               email=reg_form.cleaned_data["email"],
                                               password=make_password(reg_form.cleaned_data["password"]), )
                user.save()
                return redirect('/login')
            else:
                reason = reg_form.errors.as_json
                # To Do 非法数据越过页面校验 output server validate reason to page
                return render(request, 'register.html', locals())
        else:
            # 判断用户名是否重复
            if request.GET.get('user_name') is not None:
                validate_user_name = request.GET.get('user_name')
                validate_result = UserInfo.objects.filter(username=validate_user_name)
                validate_data = {}
                if len(validate_result) > 0:
                    validate_data = {'validate': 'duplicate'}
                else:
                    validate_data = {'validate': 'well'}
                return JsonResponse(validate_data)
            reg_form = RegForm()
    except Exception as e:
        logging.error(e)
    return render(request, 'register.html', locals())


@login_required(login_url='/login/')
def center_info(request):
    return render(request, 'user_center_info.html')


@login_required(login_url='/login/')
def center_order(request):
    return render(request, 'user_center_order.html')


@login_required(login_url='/login/')
def center_site(request):
    return render(request, 'user_center_site.html')
