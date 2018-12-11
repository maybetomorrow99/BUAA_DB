# -*- coding:utf8 -*-
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm, GoodsRegisterForm, ImgForm
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


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
                same_account_user = models.User.objects.filter(account=account)
                if same_account_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    print(1111)
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


@csrf_exempt
def view(request):
    """
    display the goods in the database on the page
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        content = {}
        goods_set = models.Goods.objects.all()

        goods = []
        for item in goods_set:
            try:
                comment_list = models.Comment.objects.filter(goods=item.id)
                goods.append({'goods': item, 'comment': comment_list})
            except models.Goods.DoesNotExist:
                print("Error")

        page_robot = Paginator(goods, 4)
        page_num = request.GET.get("page")
        try:
            goods_list = page_robot.page(page_num)
        except EmptyPage:
            goods_list = page_robot.page(1)
        except PageNotAnInteger:
            goods_list = page_robot.page(1)
        content["goods"] = goods
        content["goods_list"] = goods_list
        content["page_robot"] = page_robot
        content["total_number"]= get_num_paginator(page_robot, goods_list.number, 7)
        return render(request, 'view/view.html', content)
    else:
        return render(request, 'view/view.html')


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
    view my goods
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        content = {}
        shop_id = models.Shop.objects.filter(shop_owner=request.session['user_id'])[0].id
        goods_set = models.Goods.objects.filter(shop_id=shop_id)

        goods = []
        for item in goods_set:
            try:
                comment_list = models.Comment.objects.filter(goods=item.id)
                goods.append({'goods': item, 'comment': comment_list})
            except models.Goods.DoesNotExist:
                print("Error")

        page_robot = Paginator(goods, 4)
        page_num = request.GET.get("page")
        try:
            goods_list = page_robot.page(page_num)
        except EmptyPage:
            goods_list = page_robot.page(1)
        except PageNotAnInteger:
            goods_list = page_robot.page(1)
        content["goods"] = goods
        content["goods_list"] = goods_list
        content["page_robot"] = page_robot
        content["total_number"] = get_num_paginator(page_robot, goods_list.number, 7)
        return render(request, 'shop/shop.html', content)
    else:
        return render(request, 'shop/shop.html')


def goods_register(request):
    """
    register the item in the library
    :param request:
    :return:
    """
    if request.method == "POST":
        goods_register_form = GoodsRegisterForm(request.POST, request.FILES)
        if goods_register_form.is_valid():  # 获取数据
            shop_id = models.Shop.objects.filter(shop_owner=request.session['user_id'])[0].id
            name = goods_register_form.cleaned_data['name']
            price = goods_register_form.cleaned_data['price']
            quantity = goods_register_form.cleaned_data['quantity']
            detail = goods_register_form.cleaned_data['detail']
            category = goods_register_form.cleaned_data['category']
            img = goods_register_form.cleaned_data['img']
            new_good = models.Goods(shop_id=shop_id, name=name,price=price, quantity=quantity, validity=True,
                                    detail=detail, category=category, img_url=img)
            new_good.save()
            return redirect('/shop/')
    goods_register_form = GoodsRegisterForm()
    return render(request, 'shop/register.html', locals())


def goods_modify(request):
    """
    modify goods
    :param request:
    :return:
    """
    if request.method == "POST":
        goods_register_form = GoodsRegisterForm(request.POST, request.FILES)
        if goods_register_form.is_valid():  # 获取数据
            goods_id = request.session['cur_goods_id']
            try:
                goods = models.Goods.objects.get(id=goods_id)
            except models.Goods.DoesNotExist:
                return redirect('/col/')
            goods.name = goods_register_form.cleaned_data['name']
            goods.price = goods_register_form.cleaned_data['price']
            goods.quantity = goods_register_form.cleaned_data['quantity']
            goods.detail = goods_register_form.cleaned_data['detail']
            goods.category = goods_register_form.cleaned_data['category']
            goods.img_url = goods_register_form.cleaned_data['img']
            goods.save()
            return redirect('/shop/')
    try:
        goods_id = request.GET.get('id')
        goods_obj = models.Goods.objects.get(id=goods_id)
        goods_register_form = GoodsRegisterForm(initial={'name': goods_obj.name,
                                                         'price': goods_obj.price,
                                                        'quantity': goods_obj.quantity,
                                                        'detail': goods_obj.detail,
                                                        'category': goods_obj.category,
                                                         'img':goods_obj.img_url})
        request.session['cur_goods_id'] = goods_id  # 用session保留goods_id的访问
    except models.Goods.DoesNotExist:
        print("Error:modify")
        goods_register_form = GoodsRegisterForm()
    return render(request, 'shop/modify.html', locals())


@api_view(['GET', 'POST'])
def goods_del(request):
    """
    goods delete
    :param request:
    :return:
    """
    if request.method == 'POST':
        goods_id = request.data.get('data')
        goods_obj = models.Goods.objects.get(id=goods_id)
        goods_obj.delete()
        return render(request, 'shop/shop.html')


def col(request):
    """
    my collection
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        content = {}
        goods = models.Goods.objects.filter(shop_id=-1)
        user_id = request.session['user_id']
        goods_set = models.UserFavourites.objects.filter(user_id=user_id)
        for item in goods_set:
            goods = goods | models.Goods.objects.filter(id=item.goods_id)
        page_robot = Paginator(goods, 4)
        page_num = request.GET.get("page")
        try:
            goods_list = page_robot.page(page_num)
        except EmptyPage:
            goods_list = page_robot.page(1)
        except PageNotAnInteger:
            goods_list = page_robot.page(1)
        content["goods"] = goods
        content["goods_list"] = goods_list
        content["page_robot"] = page_robot
        content["total_number"] = get_num_paginator(page_robot, goods_list.number, 7)
        return render(request, 'col/col.html', content)
    else:
        return render(request, 'col/col.html')


@api_view(['GET', 'POST'])
def favourites_add(request):
    """
    add favourites
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.session['user_id']
        goods_id = request.data.get('data')

        same_favourites = models.UserFavourites.objects.filter(user_id=user_id, goods_id=goods_id)
        if same_favourites:
            print("不能重复添加")
            return render(request, 'view/view.html')
        new_favor = models.UserFavourites(user_id=user_id, goods_id=goods_id)
        new_favor.save()
    return render(request, 'view/view.html')


@api_view(['GET', 'POST'])
def favourites_del(request):
    """
    delete favourites
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.session['user_id']
        goods_id = request.data.get('data')

        favor_obj = models.UserFavourites.objects.get(user_id=user_id, goods_id=goods_id)
        favor_obj.delete()
        return render(request, 'col/col.html')


def order(request):
    return render(request, 'order/order.html')


@api_view(['GET', 'POST'])
def order_submit(request):
    """
    submit order
    :param request:
    :return:
    """
    if request.method == 'POST':
        buyer_id = request.session['user_id']
        goods_id = request.data.get('data')
        status = 1
        type = 0
        new_order = models.Order(buyer_id=buyer_id, goods_id=goods_id, status=status, type=type)
        new_order.save()
    return render(request, 'order/order.html')


@api_view(['GET', 'POST'])
def order_pay(request):
    """
    order pay
    :param request:
    :return:
    """
    if request.method == 'POST':
        order_id = request.data.get('data')
        models.Order.objects.filter(id=order_id).update(status=2)
        return redirect('/order/')
    return redirect('/order/')


@api_view(['GET', 'POST'])
def order_seller_confirm(request):
    """
    seller confirm order, ready for shipment
    :param request:
    :return:
    """
    if request.method == 'POST':
        order_id = request.data.get('data')
        models.Order.objects.filter(id=order_id).update(status=3)
    return redirect('/order/')


@api_view(['GET', 'POST'])
def order_buyer_confirm(request):
    """
    confirm receipt of goods
    :param request:
    :return:
    """
    if request.method == 'POST':
        order_id = request.data.get('data')
        models.Order.objects.filter(id=order_id).update(status=3)
    return redirect('/order/')


@api_view(['GET', 'POST'])
def order_cancel(request):
    if request.method == 'POST':
        order_id = request.data.get('data')
        models.Order.objects.filter(id=order_id).update(status=0)
    return redirect('/order/')


def order_view(request):
    """
    view order
    :param request:
    :return:
    """
    if request.session.get('is_login', None):
        buyer_id = request.session['user_id']
        goods_list0 = order_get_by_status(0, buyer_id)
        g0 = goods_list0.__len__()
        goods_list1 = order_get_by_status(1, buyer_id)
        g1 = goods_list1.__len__()
        goods_list2 = order_get_by_status(2, buyer_id)
        g2 = goods_list2.__len__()
        goods_list3 = order_get_by_status(3, buyer_id)
        g3 = goods_list3.__len__()

        return render(request, 'order/order.html', locals())
    else:
        return render(request, 'order/order.html')

def order_get_by_status(order_status, buyer_id):
    order_list = models.Order.objects.filter(buyer_id=buyer_id, status=order_status)
    goods_list = []
    for item in order_list:
        try:
            goods = models.Goods.objects.get(id=item.goods_id)
            goods_list.append({'goods': goods,
                               'order': item})
        except models.Goods.DoesNotExist:
            print("Error:order_get_by_status")
    return goods_list


# 这个函数没有写好
@api_view(['GET', 'POST'])
def comment(request):
    if request.method == "POST":
        detail = request.data.get('detail')
        satisfaction = request.data.get('score')

        order_id = request.data.get('id')
        print(detail,order_id,satisfaction)
        try:
            order_obj = models.Order.objects.get(id=order_id)
            goods= models.Goods.objects.get(id=order_obj.goods_id)
            new_comment = models.Comment(goods=goods, detail=detail, satisfaction=satisfaction)
            new_comment.save()
        except models.Goods.DoesNotExist:
            print("Error")

        return render(request, 'order/order.html')


def comment_view(request):
    # if request.method == "POST":
    # goods_id = request.data.get('id')
    goods_id = 18
    comment_list = models.Comment.objects.filter(goods=goods_id)
    print(comment_list)
    return render(request, 'order/order.html', locals())


def uploadImg(request): # 图片上传函数
    # if request.method == 'POST':
    #     img = models.Img(img_url=request.FILES.get('img'))
    #     img.save()
    # return render(request, 'login/imgupload.html')
    if request.method == "POST":
        img_form = ImgForm(request.POST, request.FILES)
        message = "请检查填写的内容！"
        if img_form.is_valid():  # 获取数据
            img = img_form.cleaned_data['img']
            new_img = models.Img(img_url=img)
            new_img.save()
            return redirect('login/showImg/')  # 自动跳转到登录页面
    img_form = ImgForm()
    return render(request, 'login/imgupload.html', locals())


def showImg(request):
    imgs = models.Img.objects.all() # 从数据库中取出所有的图片路径
    context = {
        'imgs' : imgs
    }
    return render(request, 'login/showImg.html', context)
