# coding:utf-8
import os
from django.shortcuts import render
from django.db.models import Max, F, Q
from django.http import HttpResponse
from win32 import win32api
from .models import *


# 获取应用程序路径
def getAppDir(appName):
    appsList = AppInfo.apps.all()
    for app in appsList:
        if appName == app.appName:
            print('应用名：' + app.appName + '  路径：' + app.appDir)
            return app.appDir
    return ("not found the path for \"%s\"") % appName


# 打开应用程序
def openApp(appDir):
    try:
        os.startfile(appDir)  # os.startfile（）打开外部应该程序，与windows双击相同
    except FileNotFoundError:
        return False
    return True


# 首页
def index(request):
    appsList = AppInfo.apps.all()
    for app in appsList:
        print('应用名：' + app.appName + '  路径：' + app.appDir)
    context = {'appsList': appsList}
    return render(request, 'software/index.html', context)

# def WeChat(request):
#     # ShellExecute(hwnd, op, file, params, dir, bShow)
#     # - hwnd: 父窗口的句柄，若没有则为0
#     # - op：要进行的操作，为open，print or 空
#     # - file：要运行的程序或脚本
#     # - params: 要向程序传递的参数，如果打开的是文件则为空
#     # - dir：程序初始化的目录
#     # - bShow：是否显示窗口
#     appName = WeChat.__name__
#     appDir = getAppDir(appName)
#     win32api.ShellExecute(0, 'open', appDir, '', '', 1)  # 打开外部应用程序的另一种方法
#     return index(request)

# 打开应用程序
def openAppHelper(request):
    if request.method=='GET':
        appName = request.GET.get('name')
        appDir = getAppDir(appName)
        print(appDir)
        flag = openApp(appDir)
        if flag:
            return index(request)
        else:
            return HttpResponse(("not found the path for \"%s\"") % appName)
    else:
        return HttpResponse("请求失败！！")