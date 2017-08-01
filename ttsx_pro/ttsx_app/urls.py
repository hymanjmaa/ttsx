# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *
__author__ = 'Hyman'
__time__ = '2017-08-01 12:43'

urlpatterns = [
    url(r'^$', index),
]


