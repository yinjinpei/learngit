# from django.shortcuts import render
# Create your views here.
from django.http import *
# from django.template import RequestContext,loader
from django.shortcuts import render
from .models import *

def index(request):
    # 方法一
    # temp=loader.get_template('booktest/index.html')
    # return HttpResponse(temp.render())
    # 方法二
    bookList={'bookName':['大话西游','演员的自我修养','ptyhon3基础']}
    # bookList={'bookName':'大话西游'}
    return render(request,'booktest/index.html',bookList)

def index_bak(request):
    return HttpResponse('<h1>您好,服务器正在维护中...</h1>')