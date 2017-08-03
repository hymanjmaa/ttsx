# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *
__author__ = 'Hyman'
__time__ = '2017-08-01 12:43'


urlpatterns = [
    url(r'^$', index),
    url(r'^register', register, name='register'),
    url(r'^login', do_login, name='login'),
    url(r'^logout', do_logout, name='logout'),
    # url('^$', center_info),
    url(r'^center_info', center_info, name='center_info'),
    url(r'^center_order', center_order, name='center_order'),
    url(r'^center_site', center_site, name='center_site'),
]


