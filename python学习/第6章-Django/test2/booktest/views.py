# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
from .models import *
# Create your views here.


def index(request):
    # list=BookInfo.books1.filter(heroinfo__hcontent__contains='八') # 获取英雄中hcontent里有'八'字的相关联书的名字
    # list=BookInfo.books1.filter(pk__lte=3)    #获取主键小于等于3的书名，pk表示primary key，默认的主键是id
    # list=BookInfo.books1.aggregate(Max('bpub_date'))    #获取日期最大的书名
    # list=BookInfo.books1.filter(bread__gt=F('bcommet')) #bcommet：评论量，bread:阅读量，F：F对象用来比较列与列，例：比较bcommet和bread

    # 获取主键（即id）少于6且书名包含'八'的书名
    # 方法一：
    # list=BookInfo.books1.filter(pk__lt=6,btitle__contains='八')
    # 方法二： 即逻辑与
    # list = BookInfo.books1.filter(pk__lt=6).filter(btitle__contains='八')

    # 逻辑或，如下:
    list=BookInfo.books1.filter(Q(pk__lt=6) | Q(bcommet__gt=10))    #查询id小于6且阅读量大于10的书名
    context={'list1':list}



    return render(request,'booktest/index.html',context)