# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
from django.http import HttpResponse
from .models import *


def index(request):
    # 练习一，获取主键为1的英雄
    # hero=HeroInfo.objects.get(pk=1)
    # hero2=HeroInfo.objects.get(hcontent='医术')
    # context={'hero':hero,'hero2':hero2}

    # 练习二，获取所有英雄
    # list=HeroInfo.objects.all()
    # context={'list':list}

    # 练习三，获取被已删除的英雄
    # list2=HeroInfo.objects.filter(isDelete=True)
    # context={'list2':list2}

    #练习四，if语法
    list3=HeroInfo.objects.filter(id__lt=10) # 获取id小于10的值   id__gt是大于
    context={'list3':list3}
    return render(request, 'booktest/index.html',context)

def show(request,id,id2):
    # 练习五，获取数字
    # 练习六，获取数字--反向解析
    listid = [id,id2]
    context = {'listid':listid}
    return render(request, 'booktest/show.html',context)

# 模板继承
def index2(request):
    return render(request, 'booktest/index2.html')

def base2_user(request,user):
    context={'user':user}
    return render(request,'booktest/base2_user.html',context)

def user1(request,user1):
    context = {'user1': user1}
    return render(request,'booktest/user1.html',context)

# html转义
def htmltest(request):
    context={'t1':'<h1>123</h1>'}
    return render(request,'booktest/htmltest.html',context)

# csrf--跨站攻击
def csrf1(request):
    return render(request,'booktest/csrf1.html')

def csrf2(request):
    uname=request.POST['uname']
    return HttpResponse(uname)