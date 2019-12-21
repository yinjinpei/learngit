# coding:utf-8
from django.shortcuts import render,redirect
import os
from django.db.models import Max, F, Q
from django.http import HttpResponse
from .models import *
import logging  # 日志
import hashlib  # 加密模块

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")


# 明文加密
def hash_code(s, salt='mysite'):    # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def index(request):
    clientIP = request.META['REMOTE_ADDR']
    print(("INFO：来自：%s, 访问用户首页") % clientIP)
    logging.info(("INFO：来自：%s, 访问用户首页") % clientIP)
    return render(request,'login/index.html')

def login(request):
    # 通过下面的if语句，我们不允许重复登录：
    if request.session.get('is_login', None):
        return render(request, 'login/index.html')
        # return redirect('user/index')

    clientIP = request.META['REMOTE_ADDR']
    print(("INFO：来自：%s, 访问用户登录页面") % clientIP)
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "验证码错误！！"

        if login_form.is_valid():
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            # django自带获取表单方式
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if username and password:  # 确保用户名和密码都不为空
                # username = username.strip()  # 去掉左右两侧连续的字符，不指定符号，删除空格，返回值为字符串
                # 用户名字符合法性验证
                # 密码长度验证
                # 更多的其它验证.....
                print('开始验证用登录户名和密码！')

                userNameList = User.userinfo.all()  # 获取数据库所有用户对象
                for user_name in userNameList:
                    if username == user_name.name:  # 检查用户名是否存在
                        if hash_code(password) == user_name.password:  # 匹配用户的密码
                            print(user_name.name, user_name.password)
                            print('登录密码验证成功！！')
                            logging.info(("INFO：来自：%s, 登录密码验证成功！！") % clientIP)
                            logging.info(("INFO：用户：%s，密码：%s") % (user_name.name,user_name.password))
                            message = "登录成功"

                            # 通过下面的语句，我们往session字典内写入用户状态和数据：
                            request.session['is_login'] = True
                            request.session['user_id'] = user_name.id
                            request.session['user_name'] = user_name.name

                            # return HttpResponse('<h1>登录成功！！</h1>') # for test
                            return render(request, 'login/index.html', {"message": message})
                        else:
                            print('登录密码不正确！！')
                            logging.error(("ERROR：来自：%s, 登录密码不正确！！") % clientIP)
                            message = "密码不正确！"
                            break
                else:
                    print('登录用户不存在！！')
                    logging.error(("ERROR：来自：%s, 登录用户不存在！！") % clientIP)
                    message = "用户名不存在！"
            # return render(request, 'login/login.html',{"message": message})
            return render(request, 'login/login.html',locals())

    logging.error(("ERROR：来自：%s, 请求失败，请求方式不是POST！") % clientIP)
    login_form = UserForm()
    return render(request, 'login/login.html',locals())

def register(request):
    print('注册')
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return render(request, 'login/index.html')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "验证码错误！！！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.userinfo.filter(name=username)  # 获取数据库所有用户对象
                print(same_name_user)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.userinfo.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = User.userinfo.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                print(new_user.name,new_user.password,new_user.email,new_user.save)
                message='注册成功!!'
                return render(request, 'login/register.html', locals())  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    print('注销')
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有退出一说
        return render(request, 'software/index.html')

    request.session.flush()
    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，
    # 那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。

    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return render(request, 'software/index.html')


