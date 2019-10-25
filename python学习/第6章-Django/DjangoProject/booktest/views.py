# from django.shortcuts import render
# Create your views here.
from django.http import *


def index(request):
    return HttpResponse('hello world!')


def index_bak(request):
    return HttpResponse('<h1>您好,服务器正在维护中...</h1>')