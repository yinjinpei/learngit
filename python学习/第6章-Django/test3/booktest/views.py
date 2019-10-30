from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

#render是HttpResponse简写
#redirect是HttpResponseRedirect简写


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

# get展示链接的页面
def getTest1(request):
    return render(request,'booktest/getTest1.html')

# get方式，接收一键一值的情况
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

# get方式，接收一键多值的情况
def getTest3(request):
    # 获取一键多个值,返回的是一个列表
    a3=request.GET.getlist('a')
    context={'a':a3}
    return render(request,'booktest/getTest3.html',context)


# post方式，接收一键一值的情况
def postTest1(request):
    return render(request,'booktest/postTest1.html')

# post方式，接收一键多值的情况
def postTest2(request):
    # 获取传递过来的单个值，方法一：
    uname=request.POST.get('uname')

    # 获取传递过来的单个值，方法二：推荐使用
    upwd=request.POST['upwd']
    ugender=request.POST['ugender']

    # 获取一键多个值,返回的是一个列表
    uhobby=request.POST.getlist('uhobby')

    context={'uname':uname,'upwd':upwd,'ugender':ugender,'uhobby':uhobby}
    return render(request,'booktest/postTest2.html',context)



#cookie练习，设置与获取
def cookieTest(request):
    response=HttpResponse()
    #设置cookie
    # response.set_cookie('t1','abc')

    #下面操作前需要设置cookie
    #接收cookie，得到字典键和键值
    cookie=request.COOKIES
    #判断't1'键和键值是否在cookie字典里
    if ('t1' in cookie.keys()):
        #写cookie
        response.write(cookie['t1'])

    return response


#子类HttpResponseRedirect：重写向
def redTest1(request):
    # return HttpResponseRedirect('/redTest2')

    #HttpResponseRedirect简写:redirect
    return redirect('/redTest2')

def redTest2(request):
    context={'detail':'这是子类HttpResponseRedirect重定向！！！简写方法:redirect'}
    return render(request,'booktest/redTest2.html',context)
