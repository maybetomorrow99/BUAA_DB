# -*- coding:utf8 -*-
from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm

def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
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
                    # request.session['user_id'] = user.id
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
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
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
    return render(request, 'col/col.html')


def order(request):
    return render(request, 'order/order.html')


def view(request):
    goods_list = models.User.objects.all()
    return render(request, 'view/view.html')


def shop(request):
    return render(request, 'shop/shop.html')

