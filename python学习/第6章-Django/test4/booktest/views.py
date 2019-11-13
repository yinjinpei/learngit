# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
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