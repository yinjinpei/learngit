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

def peter(request):
    # HttpReqeust对象:
    # 属性:path：一个字符串，表示请求的页面的完整路径，不包含域名
    return HttpResponse('输出路径使用request.path:  &nbsp&nbsp'+request.path)

# 展示链接的页面
def getTest1(request):
    return render(request,'booktest/getTest1.html')

# 接收一键一值的情况
def getTest2(request):
    # 获取传递过来的值，方法一：
    # a1=request.GET.get('a')

    # 获取传递过来的键值，方法一：推荐使用
    a1 = request.GET['a']
    b1 = request.GET['b']
    c1 = request.GET['c']
    # 构造上下文
    context={'a':a1, 'b':b1, 'c':c1}
    # 向模板中传递上下文，进行渲染
    return render(request,'booktest/getTest2.html',context)

# 接收一键多值的情况
def getTest3(request):
    a3=request.GET.getlist('a')
    context={'a':a3}
    return render(request,'booktest/getTest3.html',context)