# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin

__author__ = 'Hyman'
__time__ = '2017-08-03 1:27'


class UrlMiddleware(MiddlewareMixin):
    # def __init__(self, get_response):
    #     self.get_response = get_response
    #
    # def __call__(self, request):
    #     return self.get_response(request)

    def process_view(self, request, view_name, view_args, view_kwargs):
        # print("+++++++++++++++++++++++++++++++" + request.path)
        # print("+++++++++++++++++++++++++++++++" + request.get_full_path())
        path = request.get_full_path()
        try:
            index = path.index('next=')
            path = path[index + 6:]
        except Exception as e:
            pass
        if path not in ['/register',
                        '/login',
                        '/logout', ]:
            request.session['url_path'] = path
