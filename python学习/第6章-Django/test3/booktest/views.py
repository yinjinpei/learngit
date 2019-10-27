from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('hello index !!')

def index2(request):
    return HttpResponse('hello 只包含booktest index2 !!')

def index3(request):
    return HttpResponse('hello，包含booktest index3')


def detail(request,p1):
    return HttpResponse('<h1> hello 匹配包含数字的  '+p1+'</h1>')

def detail2(request,p1,p2,p3):
    return HttpResponse('year:%s  moth:%s  day:%s'%(p3,p2,p1))


def detail3(request,p1,p2,p3):
    return HttpResponse('year:%s  moth:%s  day:%s' % (p2, p1, p3))


