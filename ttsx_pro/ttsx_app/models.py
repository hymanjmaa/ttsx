# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 采用的继承方式扩展用户信息
class UserInfo(AbstractUser):

    ushou = models.CharField(max_length=20, default='', verbose_name='收件人')
    uaddress = models.CharField(max_length=100, default='', verbose_name='收货地址')
    uyoubian = models.CharField(max_length=6, default='', verbose_name='邮编')
    uphone = models.CharField(max_length=11, default='', verbose_name='手机')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username
