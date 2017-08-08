# -*- coding: utf-8 -*-
from datetime import datetime
import logging

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from haystack.generic_views import SearchView

from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password


# Create your views here.


def index(request):
    try:
        type_list = TypeInfo.objects.all()
        list_index = []
        for typeinfo in type_list:
            list_index.append({
                'type': typeinfo,
                'list_new': typeinfo.goodsinfo_set.order_by('-id')[:4],
                'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[:3]
            })
        return render(request, 'index.html', locals())
    except Exception as e:
        logging.error(e)
    return render(request, 'failure.html')


def list_info(request):
    try:
        rank = request.GET.get('rank', '-id')
        typeinfo = TypeInfo.objects.get(pk=request.GET.get('id'))
        list_typelist = typeinfo.goodsinfo_set.order_by(rank)
        list_new = typeinfo.goodsinfo_set.order_by('-id')[:2]

        paginator = Paginator(list_typelist, 10)

        page_index = int(request.GET.get('page', '1'))
        if page_index <= 0:
            page_index = 1
        if page_index >= paginator.num_pages:
            page_index = paginator.num_pages

        page_info = paginator.page(int(page_index))

        return render(request, 'list.html', locals())
    except Exception as e:
        logging.error(e)
    return render(request, 'failure.html')


def detail_info(request):
    try:
        gid = request.GET.get('id')
        goods_detail = GoodsInfo.objects.get(pk=gid)
        goods_detail.gclick += 1
        goods_detail.save()
        list_new = GoodsInfo.objects.filter(gtype=goods_detail.gtype).order_by('-id')[:2]

        response = render(request, 'detail.html', locals())
        # 最近浏览，数据存储格式如id1,id2,id3,id4,id5
        goods_ids = request.COOKIES.get('goods_ids', '')
        # 判断是否存在gid，如果存在则删除，然后再加到第一个，否则，直接加到第一个
        if len(goods_ids) == 0:
            goods_ids2 = [gid]
        else:
            goods_ids2 = goods_ids.split(',')
            if gid in goods_ids2:
                goods_ids2.remove(gid)
            else:
                if len(goods_ids2) == 5:
                    goods_ids2.pop()
            goods_ids2.insert(0, gid)
        response.set_cookie('goods_ids', ','.join(goods_ids2))

        return response
    except Exception as e:
        logging.error(e)
    return render(request, 'failure.html')


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
                        # TO DO 查询购物车总数量，写入session
                else:
                    reason = "1"
                    return render(request, 'login.html', locals())
                return response
            else:
                # To Do 非法数据越过页面校验 output server validate reason to page
                return render(request, 'login.html', locals())
        else:
            if request.user.is_authenticated:
                return redirect('/center_info')
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
    # 查询最近浏览商品
    goods_ids = request.COOKIES.get('goods_ids', '').split(',')
    # goods_list=GoodsInfo.objects.filter(id__in=goods_ids)
    goods_list = []
    for gid in goods_ids:
        if gid:
            goods_list.append(GoodsInfo.objects.get(id=gid))

    return render(request, 'user_center_info.html', locals())


@login_required(login_url='/login/')
def center_order(request):
    return render(request, 'user_center_order.html')


@login_required(login_url='/login/')
def center_site(request):
    try:
        if request.method == 'POST':
            post = request.POST
            user = request.user
            user.ushou = post.get('ushou')
            user.uaddress = post.get('uaddress')
            user.uphone = post.get('uphone')
            user.save()
        return render(request, 'user_center_site.html')
    except Exception as e:
        logging.error(e)
    return redirect('index')


@login_required(login_url='/login/')
def lucky(request):
    return render(request, 'lucky.html')


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context


def add_cart(request):
    try:
        dict = request.GET
        gid = int(dict.get('gid'))
        count = int(dict.get('count'))

        # TO DO 判断库存，如果大于库存，不再添加

        # 查询当前用户是否已经购买过此商品，如果未购买则创建，如果已购买则修改数量
        carts = CartInfo.objects.filter(user_id=request.user.id, goods_id=gid)
        if len(carts) == 0:
            cart = CartInfo()
            cart.user_id = request.user.id
            cart.goods_id = int(gid)
            cart.count = int(count)
            cart.save()
        else:
            cart = carts[0]
            cart.count += count
            cart.save()

        c = CartInfo.objects.filter(user_id=request.user.id).aggregate(Sum('count'))

        return JsonResponse({'isok': 1, 'count': c.get('count__sum')})
    except Exception as e:
        logging.error(e)
        return render(request, 'failure.html')


@login_required(login_url='/login/')
def cart(request):
    try:
        cart_list = CartInfo.objects.filter(user_id=request.user.id)
        return render(request, 'cart.html', locals())
    except Exception as e:
        logging.error(e)
    return render(request, 'failure.html')


@login_required(login_url='/login/')
def del_cart(request):
    try:
        cid = int(request.GET.get('cid'))
        cart = CartInfo.objects.get(pk=cid)
        cart.delete()
        return JsonResponse({'isok': 1})
    except Exception as e:
        logging.error(e)
        return JsonResponse({'isok': 0})


@login_required(login_url='/login/')
def set_cart(request):
    dict = request.GET
    cid = dict.get('cid')
    count = dict.get('count')

    isok = 0
    try:
        cart = CartInfo.objects.get(pk=cid)
        cart.count = int(count)
        cart.save()
        isok = 1
        count = cart.count
    except CartInfo.DoesNotExist as e1:
        logging.error(e1)
        isok = 0
        count = 0
    except Exception as e:
        logging.error(e)
        isok = 0
        count = cart.count
    return JsonResponse({'isok': isok, 'count': count})


@login_required(login_url='/login/')
def calc_count(request):
    # c=CartInfo.objects.filter(user_id=request.session.get('uid')).count()
    c = CartInfo.objects.filter(user_id=request.user.id).aggregate(Sum('count'))
    return JsonResponse({'count': c.get('count__sum')})


@login_required(login_url='/login/')
def order_list(request):
    pre_order = '提交订单'
    dict = request.POST
    cids = dict.getlist('cid')
    pre_order_list = CartInfo.objects.filter(pk__in=cids)
    return render(request, 'place_order.html', locals())


@login_required(login_url='/login/')
@transaction.atomic
def order_handle(request):
    sid = transaction.savepoint()

    try:
        dict = request.POST
        cids = dict.getlist('cid')
        address = dict.get('address')
        uid = request.user.id
        '''
        创建订单主表对象
        判断商品库存是否足够
        遍历购物车信息，创建订单详表
        将商品数量减少
        '''
        order = OrderInfo()
        order.oid = '%s%d' % (datetime.now().strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.ototal = 0
        order.oaddress = address
        order.save()

        cartlist = CartInfo.objects.filter(pk__in=cids)
        total = 0
        for cart in cartlist:
            if cart.count > cart.goods.gkucun:
                # 库存不足，放弃购买
                transaction.savepoint_rollback(sid)
                return redirect('/cart')
            else:
                # 库存足够，创建详单
                detail = OrderDetailInfo()
                detail.goods = cart.goods
                detail.order = order
                detail.price = cart.goods.gprice
                detail.count = cart.count
                detail.save()
                # 修改库存数量
                goods = cart.goods
                goods.gkucun -= cart.count
                goods.save()
                # 计算总价
                total += detail.price * detail.count
                # 删除购物车
                cart.delete()
        # 保存总价
        order.ototal = total + 10
        order.save()
        # 购买成功
        transaction.savepoint_commit(sid)
        return redirect('/center_order')
    except Exception as e:
        logging.error(e)
        # raise
        transaction.savepoint_rollback(sid)
        return redirect('/cart')
