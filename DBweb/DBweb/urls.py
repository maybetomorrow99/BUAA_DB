"""DBweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from trading import views
from . import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logout),
    url(r'^col/$', views.col),
    url(r'^order/$', views.order_view),
    url(r'^shop/$', views.shop),
    url(r'^view/$', views.view),
    #url(r'^view/search/$', views.search),
    url(r'^view/get_detail/$', views.get_detail),
    url(r'^view/add_favourites/$', views.favourites_add),
    url(r'^shop/register/$', views.goods_register),
    url(r'^shop/modify/$', views.goods_modify),
    url(r'^shop/goods_del/$', views.goods_del),
    url(r'^order/order_pay/$', views.order_pay),
    url(r'^order/order_cancel/$', views.order_cancel),
    url(r'^order/order_buyer_confirm/$', views.order_buyer_confirm),
    url(r'^order/comment/$', views.comment),
    url(r'^col/favourites_del/$', views.favourites_del),
    url(r'^view/order_submit/$', views.order_submit),
    url(r'uploadImg/', views.uploadImg),
    url(r'showImg/', views.showImg),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

