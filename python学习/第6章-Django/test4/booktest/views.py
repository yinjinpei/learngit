# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
from .models import *


def index(request):
    # 练习一
    # hero=HeroInfo.objects.get(pk=1)
    # hero2=HeroInfo.objects.get(hcontent='医术')
    # context={'hero':hero,'hero2':hero2}

    # 练习二
    list=HeroInfo.objects.all()
    context={'list':list}

    return render(request, 'booktest/index.html',context)