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


# 验证码
def verifyCode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random

    # 创建背景颜色,用于画面的背景色、宽、高
    bgColor=(random.randrange(50,100),random.randrange(50,100),random.randrange(50,100))
    #规定宽和高
    width=100
    height=50
    # 创建画面对象
    image=Image.new('RGB',(width,height),bgColor)
    # 构造字体对象
    font=ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf',30)
    # font = ImageFont.truetype(r'C:\Windows\Fonts\STCAIYUN.TTF', 30)
    # 构造字体颜色
    fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    # 创建画笔
    draw=ImageDraw.Draw(image)
    # 创建文本内容
    text='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 记录一个每次随机生成的验证码
    textTemp=''
    # 逐个绘制字符
    for i in  range(4):
        textTemp1=text[random.randrange(0,len(text))]
        textTemp+=textTemp1
        draw.text((i*25,0),
            textTemp1,
            fontcolor,
            font)
    request.session['code']=textTemp
    # 保存到内存流中
    from io import BytesIO
    buf=BytesIO()
    image.save(buf,'png')
    # 将内存流中的内容输出到客户端中
    return HttpResponse(buf.getvalue(),'image/png')

# 验证码验证-verifyCode方法
def verifyTest1(request):
    return render(request,'booktest/verifyTest1.html')
def verifyTest2(request):
    if request.session['code'] == request.POST['code1']:
        return HttpResponse('OK,验证成功！')
    else:
        return HttpResponse('ERROR，验证码错误！')


