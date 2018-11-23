# -*- coding:utf8 -*-
from django.db import models

# Create your models here.
class User(models.Model):
    '''用户表'''

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
