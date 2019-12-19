# coding:utf-8
from django.shortcuts import render,redirect
import os
from django.db.models import Max, F, Q
from django.http import HttpResponse

from .models import *


def index(request):
    print('首页')
    return render(request,'login/index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        print('------------------------------')

        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()  # 去掉左右两侧连续的字符，不指定符号，删除空格，返回值为字符串
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            print('开始验证用户名和密码！')
            userNameList = User.userinfo.all()  # 获取数据库所有用户对象
            for user_name in userNameList:
                if username == user_name.name:  # 检查用户名是否存在
                    if password == user_name.password:  # 匹配用户的密码
                        print(user_name.name, user_name.password)
                        print('密码验证成功！')
                        return render(request, 'login/register.html')
                    else:
                        print('密码不正确！！')
                        break
            else:
                print('用户不存在！！')
                return render(request, 'login/login.html')
    return render(request, 'login/login.html')

def register(request):
    print('注册')
    return render(request,'login/register.html')

def logout(request):
    print('注销')
    return render(request, 'login/login.html')
    # return redirect('/index/')