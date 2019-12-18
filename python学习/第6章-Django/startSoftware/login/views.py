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
    print('登录')
    return render(request,'login/login.html')

def register(request):
    print('注册')
    return render(request,'login/register.html')

def logout(request):
    print('注销')
    return redirect('/index/')