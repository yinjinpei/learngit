# coding:utf-8
import os
from django.shortcuts import render,redirect
from django.db.models import Max, F, Q
from django.http import HttpResponse
# from win32 import win32api
from .models import *
from django.http import FileResponse
from django.utils.encoding import escape_uri_path


import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")


# 获取应用程序路径
def getAppDir(appName):
    appsList = AppInfo.apps.all()
    for app in appsList:
        if appName == app.appName:
            print('应用名：' + app.appName + '  路径：' + app.appDir)
            return app.appDir
    logging.error(("ERROR：%s应用程序路径找不到！！！")%appName)
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
    clientIP = request.META['REMOTE_ADDR']
    print(clientIP)
    webName = index.__name__
    print((("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName)))
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") %(clientIP,webName))

    # 已登录状态：
    if request.session.get('is_login', None):
        appsList = AppInfo.apps.filter(userName=request.session['user_name'] )  # 获取数据库所有符合筛选的用户对象
        # appsList = AppInfo.apps.all()
        if appsList:
            for app in appsList:
                print('应用名：' + app.appName + '  路径：' + app.appDir)
            context = {'appsList': appsList}
            return render(request, 'software/index.html', context)
    return render(request, 'software/index.html')


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

# 用户打开应用请求处理
def openAppHelper(request):
    clientIP = request.META['REMOTE_ADDR']
    print(clientIP)
    if request.method=='GET':
        appName = request.GET.get('name')  # 获取应用英文名即name参数
        if appName is None:
            return index(request)
        appDir = getAppDir(appName)
        logging.info("打开应用程序："+appDir)
        flag = openApp(appDir)
        if flag:
            return index(request)
        else:
            logging.error(("ERROR：来自：%s, %s应用程序找不到！！！") %(clientIP,appName))
            return HttpResponse(("not found the path for \"%s\" <hr><a href='/'>返回首页</a>") % appName)
    else:
        logging.error(("ERROR：来自：%s, 请求失败，请求方式不是GET！")%clientIP)
        return HttpResponse("请求失败！！<hr><a href='/'>返回首页</a>")

def addSoftware(request):
    print('========添加常用软件快捷键=========')
    if request.method == "POST":
        addApp_form = AddSoftware(request.POST)
        if addApp_form.is_valid():  # 看seld.errors中是否值，只要有值就是flase
            ChineseName = addApp_form.cleaned_data['ChineseName']
            EnglishName = addApp_form.cleaned_data['EnglishName']
            SoftwarePath = addApp_form.cleaned_data['SoftwarePath']
            if ChineseName and EnglishName and SoftwarePath:
                same_name_user = AppInfo.apps.filter(userName=request.session['user_name'])  # 获取数据库所有用户对象
                for user in same_name_user:
                    if EnglishName == user.appName:
                        message = "软件已存在！！"
                        return render(request, 'software/addSoftware.html', locals())
                    if ChineseName == user.remark:
                        message = "中文名重复，请取新的名字！！"
                        return render(request, 'software/addSoftware.html', locals())
                newApp = AppInfo.apps.create()
                newApp.userName = request.session['user_name']
                newApp.appName = EnglishName
                newApp.remark = ChineseName
                newApp.appDir = SoftwarePath
                newApp.save()
                message = "添加成功！"
                print(message)
    addApp_form = AddSoftware()
    return render(request, 'software/addSoftware.html', locals())
    # return redirect('/addSoftware')

def delSoftware(request):
    print('delApp_form')
    if request.method == "GET":
        same_name_user = AppInfo.apps.all()
        print(request.session['user_name'])
        appNameList=[]
        for user in same_name_user:
            if user.userName == request.session['user_name']:
                appNameList.append(user.remark)
        print(appNameList)
        message=appNameList
        delApp_form = DelSoftware()
        return render(request, 'software/delSoftware.html', locals())

    if request.method == "POST":
        delApp_form = DelSoftware(request.POST)
        if delApp_form.is_valid():  # 看seld.errors中是否值，只要有值就是flase
            ChineseName = delApp_form.cleaned_data['ChineseName']
            currentUser = request.session['user_name']
            newApp = AppInfo.apps.filter(userName=currentUser)
            if newApp:
                for app in newApp:
                    print(app)
                    if app.remark == ChineseName:
                        app.delete()    # 删除数据库对象

            same_name_user = AppInfo.apps.all() # 获取所有对象显示到页面
            appNameList = []
            for user in same_name_user:
                if user.userName == request.session['user_name']:
                    appNameList.append(user.remark)
            print(appNameList)
            message = appNameList
    delApp_form = DelSoftware()
    return render(request, 'software/delSoftware.html', locals())


def delFile(request):
    message = '请选择上传文件！'
    path = 'uploads/' + request.session['user_name'] + '/'  # 文件储存位置
    fileList = os.listdir(path)
    if not os.path.exists(path):  # 目录不存在则创建
        os.makedirs(path)
    if request.method == "POST":
        delFile_form = DelFile(request.POST)
        if delFile_form.is_valid(): # 如果有数据
            FileName = delFile_form.cleaned_data['FileName']    # 获取删除的文件名
            if os.path.exists(path+FileName):
                os.remove(path+FileName)
                delfile_message="删除成功！！"
    fileList = os.listdir(path)
    delFile_form = DelFile()
    return render(request, 'software/uploadFile.html', locals())


def uploadFile(request):
    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【文件管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    delFile_form = DelFile()  # 宣染删除表格，即宣染删除功能的输入框
    path = 'uploads/'+request.session['user_name']+'/'  # 上传文件路径，相对路径，在项目根目录下
    if not os.path.exists(path):    #目录不存在则创建
        os.makedirs(path)
    fileList = os.listdir(path)
    # 判断上传是否为空
    try:
        request.FILES['file']
    except:
        message = '请选择上传文件！'
        return render(request, 'software/uploadFile.html', locals())

    if request.method == 'POST':
        fileName=str(request.FILES['file']) # 上传的文件名
        file=request.FILES['file']  #上传的文件对象
        print(path+fileName)
        if os.path.exists(path+fileName):
            message='文件已存在，请重命名再上传！'
            return render(request, 'software/uploadFile.html', locals())
        with open(path + fileName, 'wb+')as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        message="上传成功！！"
    else:
        message='请选择上传文件！'
        print(message)

    fileList = os.listdir(path)
    return render(request, 'software/uploadFile.html', locals())


def downloadFile(request):
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        filename = request.GET.get('name')
        file = open(path+filename,'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = "attachment;filename=%s"%filename #下载带中文文件名时会有乱码，解决如下：
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
            # IE浏览器，采用URLEncoder编码
            # Opera浏览器，采用filename * 方式
            # Safari浏览器，采用ISO编码的中文输出
            # Chrome浏览器，采用Base64编码或ISO编码的中文输出
            # FireFox浏览器，采用Base64或filename * 或ISO编码的中文输出
        return response