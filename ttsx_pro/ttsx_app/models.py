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


class TypeInfo(models.Model):
    # 分类名称
    ttitle = models.CharField(max_length=20, verbose_name='商品类型')
    # 是否删除
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '商品类型信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    # 商品名称
    gtitle = models.CharField(max_length=20, verbose_name='商品名称')
    # 图片
    gpic = models.ImageField(upload_to='goods', verbose_name='商品图片')
    # 单价
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='商品单价')
    # 是否删除
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    # 单位
    gunit = models.CharField(max_length=20, default='500g', verbose_name='计量单位')
    # 点击量，人气
    gclick = models.IntegerField(verbose_name='点击量')
    # 简介
    gjianjie = models.CharField(max_length=200, verbose_name='商品简介')
    # 库存量
    gkucun = models.IntegerField(verbose_name='商品库存')
    # 描述
    gcontent = models.TextField(verbose_name='商品描述')
    # 类型
    gtype = models.ForeignKey(TypeInfo, verbose_name='商品类型')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.gtitle
