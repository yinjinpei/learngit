# coding:utf-8
from django.shortcuts import render
from .models import *
# Create your views here.


def index(request):
    list=BookInfo.books1.filter(heroinfo__hcontent__contains='八')
    context={'list':list}
    return render(request,'booktest/index.html',context)