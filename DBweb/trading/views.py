# -*- coding:utf8 -*-
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm,goodsRegisterForm
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET', 'POST'])
def get_detail(request):
    if request.method == 'POST':
        info = request.data.get('data')
        inf = request.data
        print(info)
        print(inf)
    return render(request, 'view/view.html')


def index(request):
    """
    initial page
    :param request:
    :return:
    """
    pass
    return render(request, 'login/index.html')


def login(request):
    """
    user login
    :param request:
    :return:
    """

    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)  # 绑定form
        message = "请检查填写的内容！"
        if login_form.is_valid():
            account = login_form.cleaned_data['account']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(account=account)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    """
    user register
    :param request:
    :return:
    """

    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            name = register_form.cleaned_data['name']
            account = register_form.cleaned_data['account']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            mobile_number = register_form.cleaned_data['mobile_number']
            address = register_form.cleaned_data['address']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_account_user = models.User.objects.filter(name=account)
                if same_account_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User(name=name, account=account, password=password1, mobile_number=mobile_number,
                                       credit=0, address=address)
                # new_user.name = name
                # new_user.account = account
                # new_user.password = password1
                # new_user.mobile_number = mobile_number
                # new_user.address = address
                # new_user.credit = credit
                new_user.save()

                # 添加用户对应的店铺
                new_shop = models.Shop(shop_owner=new_user.id)
                new_shop.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    """
    user logout
    :param request:
    :return:
    """

    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
    # test git
    # test git2
    # test git3


def col(request):
    """
    collection
    :param request:
    :return:
    """
    return render(request, 'col/col.html')


def order(request):
    view(request)
    return render(request, 'order/order.html')


@csrf_exempt
def view(request):
    """
    display the goods in the database on the page
    :param request:
    :return:
    """

    # goods_list = models.Goods.objects.all()
    # return render(request, 'view/view.html', {'goods_list': goods_list})
    content = {}
    goods = models.Goods.objects.all()
    page_robot = Paginator(goods, 4)
    page_num = request.get("page")
    try:
        goods_list = page_robot.page(page_num)
    except EmptyPage:
        goods_list = page_robot.page(1)
    except PageNotAnInteger:
        goods_list = page_robot.page(1)
    content["goods"] = goods
    content["goods_list"] = goods_list
    content["page_robot"] = get_num_paginator(page_robot, goods_list.number, 7)
    return render(request, 'view/view.html', content)


def get_num_paginator(page_robot, num, total):
    """
    分页函数
    :param page_robot:
    :param num:
    :param total:
    :return:
    """

    if page_robot.num_pages < total:
        return page_robot.page_range
    left_right = total//2
    num_index = page_robot.page_range.index(num)
    if num_index < left_right:
        return page_robot.page_range[0: total]
    elif page_robot.num_pages - num_index - 1 < left_right:
        return page_robot.page_range[-total:]
    else:
        return page_robot.page_range[num_index - left_right: num_index + left_right + 1]


def shop(request):
    """

    :param request:
    :return:
    """
    return render(request, 'shop/shop.html')


def good_register(request):
    """
    register the item in the library
    :param request:
    :return:
    """

    if request.method == "POST":
        good_register_form = goodsRegisterForm(request.POST)
        if good_register_form.is_valid():  # 获取数据
            shop_id = models.Shop.objects.filter(shop_owner=request.session['user_id'])[0].id
            price = good_register_form.cleaned_data['price']
            quantity = good_register_form.cleaned_data['quantity']
            detail = good_register_form.cleaned_data['detail']
            category = good_register_form.cleaned_data['category']
            new_good = models.Goods(shop_id=shop_id, price=price, quantity=quantity, validity=True,
                                    detail=detail, category=category)
            new_good.save()
            return redirect('/shop/')
    good_register_form = goodsRegisterForm()
    return render(request, 'shop/register.html', locals())


