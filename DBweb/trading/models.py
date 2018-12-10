# -*- coding:utf8 -*-
from django.db import models


# Create your models here.
class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=128)
    account = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    credit = models.IntegerField(null=True)
    mobile_number = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    img_src = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Shop(models.Model):
    """
    商铺表
    """
    shop_owner = models.IntegerField()


class Goods(models.Model):
    """
    商品表
    """
    name = models.CharField(max_length=256, default="")
    shop_id = models.IntegerField()
    price = models.FloatField()
    quantity = models.IntegerField()
    validity = models.BooleanField()
    detail = models.CharField(max_length=256)
    category = models.CharField(max_length=256)


class UserFavourites(models.Model):
    """
    收藏夹
    """
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    c_time = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    """
    订单表
    """
    submit_time = models.DateTimeField(auto_now_add=True)
    buyer_id = models.IntegerField()
    goods_id = models.IntegerField()

    # 0 订单被取消 1 卖家未确认，待支付 2 买家确认，已支付,等待收货 3 订单完成
    status = models.IntegerField()
    type = models.IntegerField()    # 0购买， 1 租赁


class Img(models.Model):
    img_url = models.ImageField(upload_to='img')


class Comment(models.Model):
    goods_id = models.ForeignKey(
        'Goods',
        on_delete=models.CASCADE,
    )
    detail = models.CharField(max_length=256)
    satisfaction = models.IntegerField()
    comment_time = models.DateTimeField(auto_now_add=True)

