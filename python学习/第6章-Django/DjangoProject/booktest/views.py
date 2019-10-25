# from django.shortcuts import render
# Create your views here.
from django.http import *
from django.template import RequestContext,loader

def index(request):
    temp=loader.get_template('booktest/index.html')
    return HttpResponse(temp.render())


def index_bak(request):
    return HttpResponse('<h1>您好,服务器正在维护中...</h1>')