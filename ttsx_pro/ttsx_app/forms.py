# -*- coding: utf-8 -*-
from django import forms

__author__ = 'Hyman'
__time__ = '2017-08-01 16:31'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", "class":"name_input", }),
                               max_length=20, min_length=5, error_messages={"required": "用户名不能为空", })
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", "class": "pass_input"}),
                               max_length=20, min_length=8, error_messages={"required": "密码不能为空", })


class RegForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "请输入用户名", "required": "required", "id": "user_name"}),
        max_length=20, min_length=5, error_messages={"required": "用户名不能为空", })
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "请输入邮箱", "required": "required", "id": "email"}),
        max_length=30, error_messages={"required": "Email不能为空", })
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "请输入密码", "required": "required", "id": "pwd"}),
        max_length=40, min_length=8, error_messages={"required": "密码不能为空", })
    passwordc = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "请再次输入密码", "required": "required", "id": "cpwd"}),
        max_length=40, min_length=8, error_messages={"required": "密码不能为空", })
