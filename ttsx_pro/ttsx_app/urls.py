# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf import settings
from django.views import static

from .upload import upload_image
from .views import *
__author__ = 'Hyman'
__time__ = '2017-08-01 12:43'


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register', register, name='register'),
    url(r'^login', do_login, name='login'),
    url(r'^logout', do_logout, name='logout'),
    url(r'^center_info', center_info, name='center_info'),
    url(r'^center_order', center_order, name='center_order'),
    url(r'^center_site', center_site, name='center_site'),
    url(r'^list_info', list_info, name='list_info'),
    url(r'^detail_info', detail_info, name='detail_info'),
    url(r'^lucky', lucky, name='lucky'),
    url(r"^uploads/(?P<path>.*)$", static.serve, {"document_root": settings.MEDIA_ROOT, }),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^search/?$', MySearchView.as_view(), name='search'),
]


