from django.shortcuts import render

# Create your views here.

# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
from django.http import HttpResponse
from .models import *
from win32 import win32api
import os

class app(object):
    def __init__(self,appDir,):
        self.appDir=appDir
    def startApp(self):
        os.startfile(self.appDir)  # os.startfile（）打开外部应该程序，与windows双击相同

def index(request):
    list='<ul>    <li>1</li>    <li>2</li>    <li>3</li></ul>'
    context={'list3':list}
    return render(request, 'software/index.html',context)

def WeChat(request):
    # ShellExecute(hwnd, op, file, params, dir, bShow)
    # - hwnd: 父窗口的句柄，若没有则为0
    # - op：要进行的操作，为open，print or 空
    # - file：要运行的程序或脚本
    # - params: 要向程序传递的参数，如果打开的是文件则为空
    # - dir：程序初始化的目录
    # - bShow：是否显示窗口
    win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe','', '', 1)
    context = {'list3': 'abc'}
    return render(request, 'software/index.html', context)

def navicat(request):
    appDir=r'E:\应用程序\Navicat Premium 12\navicat.exe1'
    try:
        os.startfile(appDir)  # os.startfile（）打开外部应该程序，与windows双击相同
    except FileNotFoundError:
        return HttpResponse('找不到应用！！')
    context = {'list3': 'abc'}
    return render(request, 'software/index.html', context)