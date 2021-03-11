# coding:utf-8
import os
import sys
import zipfile
import re
import time
import datetime
# import redis
from django.shortcuts import render,redirect
from django.db.models import Max, F, Q
from django.http import HttpResponse
# from win32 import win32api
from .models import *
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
# from dwebsocket.decorators import accept_websocket, require_websocket
import paramiko
# 使用临时文件
from django.core.files.temp import NamedTemporaryFile
# Django不支持range函数
from django.template.defaulttags import register
from urllib import parse
from threading import Thread
import ast
import logging
import configparser
import shutil
import hashlib
import json
import requests
import time
import urllib

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# 判断 X年X月X号 是不是节假日
from chinese_calendar import is_workday, is_holiday

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

# 创建定时任务实例
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
# 调试器开始
scheduler.start()


# print('-' * 50 + '获取所有任务 starting ' + '-' * 50)
# print(scheduler.get_jobs())
# print('-' * 50 + '获取所有任务 end ' + '-' * 50)

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")


# 获取配置
class getConfig(object):
    def __init__(self,path):
        '''
        :param section: 节点名
        :param path: 配置文件路径
        :param key: 变量名
        :param value: key值
        '''
        self.path = path
        self.config = configparser.ConfigParser()  # 读配置
        self.config.read(self.path, encoding='UTF-8')

    # 获取所有 sections , 注意会过滤掉[DEFAULT], 以列表形式返回
    def get_section(self):
        return self.config.sections()

    # 获取指定 section 的 keys
    def get_keys(self, section):
        return self.config.options(section)

    # 获取指定 key 的 value,以字符串形式串返回
    def get_value(self, section, key):
        return self.config.get(section, key)

    # 获取指定 key 的 value(value必须是整数类型),返回为int类型
    def getint_value(self, section, key):
        return self.config.getint(section, key)

    # 获取指定 key 的 value(value必须是浮点数类型),返回为float类型
    def getfloat_value(self, section, key):
        return self.config.getfloat(section, key)

    # 获取指定 key 的 value(value必须是布尔数类型),返回为boolean类型
    def getboolean_value(self, section, key):
        return self.config.getboolean(section, key)

    # 获取指定 section 的 keys & values
    def get_items(self, section):
        return self.config.items(section)  # 注意items()返回的字符串会全变成小写

    # 检查section（节点）是否存在
    def check_section(self, section):
        return section in self.config

    # 检查section（节点）下的key 是否存在
    def check_key(self, section, key):
        return key in self.config[section]
        # 检查section（节点）下的key的value值是否包含self.value，类似字符串匹配

    def check_value(self, section, key, value):
        return value in self.config[section][key]

    # 添加节点
    def add_section(self, section):
        try:
            self.config.add_section(section)
            return True
        except:
            return False
    # 添加 key 和 value
    def set_section(self, section, key, value):
        try:
            self.config.set(section,key,value)
            return True
        except:
            return False

    # 删除节点
    def remove_section(self,section):
        try:
            self.config.remove_section(section)
            return True
        except:
            return False

    # 删除节点中的key和value
    def remove_key(self, section, key):
        try:
            self.config.remove_option(section, key)
            return True
        except:
            return False

    # 清空除[DEFAULT]之外所有内容
    def clear(self):
        try:
            self.config.clear()
            return True
        except:
            return False

    # 保存并写入数据到配置文件中
    def save(self):
        try:
            self.config.write(open(self.path, 'w', encoding='UTF-8'))
            return True
        except:
            return False

# 字符串去空格、中文逗号转英文逗号
def replaceName(str_name):
    str_name=str_name.replace(" ","")
    str_name=str_name.replace("，",",")
    return str_name


def logoutSuperManager(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(logoutSuperManager.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    try:
        del request.session['manager_islogin']
        return render(request, 'software/index.html')
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())


# 检查是否登录超级管理用户
def loginSuperManager(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(loginSuperManager.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    manager = ManagerForm()
    setpassword = SetPasswordForm()

    if request.session.get('manager_islogin', None):
        # print('manager_islogin值：',request.session.get('manager_islogin', None))
        manager_islogin = True
    else:
        # 如果用户的二级密码在数据库中有数据了就不是首次登录
        # print('如果用户的二级密码在数据库中有数据了就不是首次登录')
        try:
            managers = ManagerDate.managers.get(user=request.session['user_name'])
            print('不是首次登录！')
            message = '请输入二级密码！'
            first_login = False
        except:
            message='首次登录，请输入二级密码！'
            print('是首次登录！')
            first_login = True

        # 要求用户输入二级密码并处理，保存至cokie
        if request.method == "POST":
            # print('要求用户输入二级密码并处理，保存至cokie')
            manager_islogin = False
            try:
                managers = ManagerDate.managers.get(user=request.session['user_name'])
                manager_from = ManagerForm(request.POST)
                if manager_from.is_valid():
                    if managers.password == manager_from.cleaned_data['password']:
                        manager_islogin = True
                        request.session['manager_islogin'] = True
                        return render(request, 'software/index.html')
                    else:
                        message = '密码错误！'
            except:
                # 首次登录时，要求用户设置二级密码并写入数据库中
                print('首次登录时，要求用户设置二级密码并写入数据库中')
                first_login = True
                setpassword_from = SetPasswordForm(request.POST)
                if setpassword_from.is_valid():
                    newManager = ManagerDate.managers.create()
                    newManager.user = request.session['user_name']
                    if setpassword_from.cleaned_data['password1'] == setpassword_from.cleaned_data['password2']:
                        newManager.password = setpassword_from.cleaned_data['password1']
                        newManager.save()
                        first_login = False
                    else:
                        message = '两次密码不一致！'

        return render(request, 'software/loginSuperManager.html', locals())
    return render(request, 'software/index.html')


# 获取应用程序路径
def getAppDir(appName):
    appsList = AppInfo.apps.all()
    for app in appsList:
        if appName == app.appName:
            # print('应用名：' + app.appName + '  路径：' + app.appDir)
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
    webName = index.__name__
    print((("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName)))
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") %(clientIP,webName))

    # 已登录状态，此功能已废弃：
    # if request.session.get('is_login', None):
    #     appsList = AppInfo.apps.filter(userName=request.session['user_name'] )  # 获取数据库所有符合筛选的用户对象
    #     # appsList = AppInfo.apps.all()
    #     if appsList:
    #         for app in appsList:
    #             print('应用名：' + app.appName + '  路径：' + app.appDir)
    #         context = {'appsList': appsList}
    #         return render(request, 'software/index.html', context)
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
    webName = str(openAppHelper.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

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
    clientIP = request.META['REMOTE_ADDR']
    webName = str(addSoftware.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    # print('========添加常用软件快捷键=========')
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
                # 如果提示某字段不能为空，请到数据库手工修改可以为空值，即把：不是null 的勾去掉
                newApp = AppInfo.apps.create()
                newApp.userName = request.session['user_name']
                newApp.appName = EnglishName
                newApp.remark = ChineseName
                newApp.appDir = SoftwarePath
                newApp.save()
                message = "添加成功！"
                # print(message)
    addApp_form = AddSoftware()
    return render(request, 'software/addSoftware.html', locals())
    # return redirect('/addSoftware')

def delSoftware(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(delSoftware.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if request.method == "GET":
        same_name_user = AppInfo.apps.all()
        # print(request.session['user_name'])
        appNameList=[]
        for user in same_name_user:
            if user.userName == request.session['user_name']:
                appNameList.append(user.remark)
        # print(appNameList)
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
                    # prapp)
                    if app.remark == ChineseName:
                        app.delete()  # 删除数据库对象

            same_name_user = AppInfo.apps.all()  # 获取所有对象显示到页面
            appNameList = []
            for user in same_name_user:
                if user.userName == request.session['user_name']:
                    appNameList.append(user.remark)
            # print(appNameList)
            message = appNameList
    delApp_form = DelSoftware()
    return render(request, 'software/delSoftware.html', locals())


def up_one_level(dirname):
    # print('上一层,dirname的值：',dirname)
    if dirname[-1] == '/':
        dirname = dirname[:-1]
    # 上一层目录完整路径
    up_one_level_path_tmp = ''
    result = dirname.split('/')
    for i in range(len(result) - 1):
        up_one_level_path_tmp += result[i] + '/'

    # print('上一层目录为：',up_one_level_path_tmp[:-1])
    return up_one_level_path_tmp[:-1]


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if dir_list:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序降序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse=True)
    # print('dir_list: ',dir_list)
    return dir_list

def downloadFileInfo(path):
    fileObjectList = [] # 存放文件对象
    dirObjectList = []  # 存放目录对象

    fileList=os.listdir(path)

    # 获取的文件或目录按照最后修改时间顺序降序排列
    fileList2 = get_file_list(path)

    class DownloadFileObject(object):
        def __init__(self, name, size, creatTime, path):
            self.downloadFileName = name
            self.downloadFileSize = size
            self.downloadFileCreaTime = creatTime
            self.downloadFileDirRoot = path

    class AbsolutePath(object):
        def __init__(self, name, dirpath):
            # 目录名
            self.DirName = name
            # 目录完整路径
            self.DirAbsolutePath = dirpath

    for file in fileList:
        if os.path.isfile(path + file):
            pass
            # print('【%s】:这是一个文件' % file)
        elif os.path.isdir(path + file):
            # print('【%s】：这是一个目录' % file)
            dirObject=AbsolutePath(file, path + file)
            dirObjectList.append(dirObject)
        else:
            pass
            # print('path:',path)
            # print('file',file)
            # print('未知文件，无法识别该文件！！')

    for file in fileList2:
        if os.path.isfile(path + file):
            # print('【%s】:这是一个文件' % file)
            filepath = path + file
            # print('文件完整路径：【%s】' % filepath)

            fileSize = os.path.getsize(filepath)  # 获取文件大小
            fileSize = fileSize / float(1024)
            fileSize = round(fileSize, 2)

            fileCreatTime = os.path.getmtime(filepath)  # 获取文件修改时间
            fileCreatTime = datetime.datetime.fromtimestamp(fileCreatTime)
            fileCreatTime = fileCreatTime.strftime('%Y-%m-%d %X')

            fileObject = DownloadFileObject(file, fileSize, fileCreatTime, path)  # 创建文件对象
            fileObjectList.append(fileObject)  # 把文件对象存放到列表

        elif os.path.isdir(path + file):
            pass
            # print('【%s】：这是一个目录' % file)
        else:
            pass
            # print('path:', path)
            # print('file', file)
            # print('未知文件，无法识别该文件！！')

    return fileObjectList, dirObjectList

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_dir,output_filename):
    zipf = zipfile.ZipFile(output_dir + '/' + output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

def zipDir(sourcePath, outFullName, password=None):
    '''
    压缩指定文件夹
    :param sourcePath: 目标文件夹路径
    :param outFullName: 保存路径+xxx.zip
    :param password: 加密密码
    :return:
    '''
    if password:
        cmd = "zip -P %s -r %s %s" % (password, outFullName, sourcePath)
    else:
        cmd = "zip -r %s %s" % (outFullName, sourcePath)
    # 执行系统命令
    status = os.popen(cmd)

    return outFullName

def match_productionMaterials(user_name,domain_name,file_path):
    '''
    :param user_name: 登录用户名
    :param domain_name: 领域名
    :param file_path: 文件的完整路径
    :return: 返回字典
    '''

    # 获取版本号
    version = file_path.split('/')[-1].split('（')[0]
    if version is None:
        version = domain_name

    # 获取所有文件名
    file_list = os.listdir(file_path)
    if len(file_list) == 0:
        return False# 获取版本号
    version=file_path.split('/')[-1].split('（')[0]
    if version is None:
        version=domain_name


    # 获取所有文件名
    file_list = os.listdir(file_path)
    if len(file_list) == 0:
        return False

    report_config = configparser.ConfigParser()
    report_config.read('config/software_config/report_check_list_config.ini', encoding='UTF-8')

    # 获取领域所需要检查的报告
    check_report = report_config.get('report_check_list', domain_name)
    if len(check_report) == 0:
        return False
    # 去空格
    check_report = check_report.strip()
    # 把字符串(配置)转换为列表
    check_report = check_report.split(',')

    print('---------------------------------------------------')
    print('%s检查报告列表：%s' % (domain_name, check_report))
    print('---------------------------------------------------')

    # 获取所有检查报告，不分前后端
    all_check_report = report_config.get('report_check_list', 'all')
    # 去空格
    all_check_report = all_check_report.strip()
    # 把字符串(配置)转换为列表
    all_check_report = all_check_report.split(',')

    all_check_report.insert(0, '版本号')

    # 初始化，把所有检查的报告都初始化为X，类型为字典，key为报告类型名、value为X
    all_check_report_dict = {}
    for report in all_check_report:
        all_check_report_dict[report] = 'X'

    for report in all_check_report:
        try:
            findStr = report_config.get('match_keywords', report)
            # print('%s 的匹配关键字：'%report,findStr)
        except Exception as e:
            # print(e)
            # print('本次匹配没有匹配到对应的报告类型！')
            continue

        for file in file_list:
            matchStr = re.findall(findStr, str(file), re.M | re.I | re.S)
            if matchStr:
                # print('【%s】:【%s】 报告已上传！！' % (report,file))
                all_check_report_dict[report] = '✔'
                break

            # try:
            #     matchStr = re.match("(.*)%s(.*)" % report, str(file), re.M | re.I | re.S)
            #     print('【%s】 报告已上传！！'%matchStr.group())
            #     all_check_report_dict[report]='✔'
            #     break
            # except:
            #     continue

    # 筛选出不涉及的相关测试报告
    uncheck_report = list(set(all_check_report).difference(check_report))
    for report in uncheck_report:
        all_check_report_dict[report] = '不涉及'
    # print('uncheck_report 数据类型：', type(uncheck_report))
    # print('不涉及的相关测试报告：', uncheck_report)

    all_check_report_dict['版本号'] = version
    # print('%s 领域收集投产材料情况：%s'%(version, all_check_report_dict))

    return all_check_report_dict

def delFile(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(delFile.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    user_management_config = getConfig('config/software_config/user_management_config.ini')
    # 黑名单目录下不显示上传功能
    versionManagerUsers = user_management_config.get_value('user_list', 'black_user_list').split(',')
    # print('删除文件')

    user_home = 'uploads/' + request.session['user_name'] + '/'
    if request.session['user_name'] in versionManagerUsers:
        # print('登录的用户名是：', request.session['user_name'])
        shar_dir_list = []  # shar用户家目录的文件夹列表

        for user in versionManagerUsers:
            shar_dir_list.append('uploads/' + user + '/')

        for dir in os.listdir(user_home):
            if os.path.isdir(user_home + dir):
                shar_dir_list.append(user_home + dir + '/')
        # print('不在这些目录下展示上传功能：', shar_dir_list)

    if request.method == "POST":
        user_home = 'uploads/' + request.session['user_name'] + '/'
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        # print('删除文件使用POST方式')

        dirname = request.GET.get('dirname')
        if dirname:
            # print('dirname确实存在！！！！！！！！',dirname)
            if dirname[-1] == '/':
                dirname = dirname[:-1]

            if request.session['user_name'] in versionManagerUsers:
                if len(dirname.split('/')) == 4:
                    domain_name = dirname.split('/')[2]
                    temp_domain_name = domain_name.split('（')[0]
                    file_path = dirname
                    try:
                        all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                          temp_domain_name, file_path)
                    except:
                        pass

            path=dirname+'/'
        # print('~~~~~~~~~~~~~~~dirname：', dirname)

        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'

        downloadFileName = request.POST.get('downloadFileName')
        # print('===================----------------=======================')
        # print(downloadFileName)
        # print('===================----------------=======================')
        if downloadFileName is not None:
            lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
            if lockbaseinfo:
                islock = lockbaseinfo[0].islock
                if islock:
                    message = "已锁库，禁止上传和删除！"
                else:
                    if os.path.exists(downloadFileName):
                        os.remove(downloadFileName)
                        str_list = downloadFileName.split('/')
                        del_file_message = "【%s】 删除成功！！" % str_list[len(str_list) - 1]
            else:
                if os.path.exists(downloadFileName):
                    os.remove(downloadFileName)
                    str_list = downloadFileName.split('/')
                    del_file_message = "【%s】 删除成功！！" % str_list[len(str_list) - 1]

            if dirname:
                print('dirname不是空值：', dirname)

                if request.session['user_name'] in versionManagerUsers:
                    if len(dirname.split('/')) == 4:
                        print('******************** 不是空值 ********************')
                        domain_name = dirname.split('/')[2]
                        file_path = dirname
                        try:
                            all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                              domain_name, file_path)
                        except:
                            pass

                up_one_level_path = up_one_level(dirname)
                dirList_is_not_null = '在模板显示返回上一层，仅作标志'

                if dirname[-1] == '/':
                    dirname = dirname[:-1]
                path = dirname + '/'

        deleted_dir_name = request.POST.get('deleted_dir_name')
        # print('===================----------------=======================')
        # print(deleted_dir_name)
        # print('===================----------------=======================')
        if deleted_dir_name is not None:
            if os.path.exists(path+deleted_dir_name):
                shutil.rmtree(path=path+deleted_dir_name)

            if dirname != 'None':
                # print('dirname不是空值：',dirname)

                if request.session['user_name'] in versionManagerUsers:
                    if len(dirname.split('/')) == 4:
                        # print('******************** 不是空值 ********************')
                        domain_name = dirname.split('/')[2]
                        file_path = dirname
                    try:
                        all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                               domain_name, file_path)
                    except:
                        pass

                up_one_level_path = up_one_level(dirname)
                dirList_is_not_null = '在模板显示返回上一层，仅作标志'

                if dirname[-1] == '/':
                    dirname = dirname[:-1]
                path = dirname + '/'

        delFile_form = DelFile(request.POST)
        if delFile_form.is_valid(): # 如果有数据
            # print('有删除数据提交！！！')
            dirname = request.POST.get('dirname')
            # print('dirname  POST方式的值是',dirname)
            if dirname:
                up_one_level_path = up_one_level(dirname)
                dirList_is_not_null = '在模板显示返回上一层，仅作标志'

                if dirname[-1] == '/':
                    dirname = dirname[:-1]

                    if request.session['user_name'] in versionManagerUsers:
                        if len(dirname.split('/')) == 4:
                            print('******************** 不是空值 ********************')
                            domain_name = dirname.split('/')[2]
                            file_path = dirname
                            try:
                                all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                                   domain_name, file_path)
                            except:
                                pass

            path = dirname + '/'

            FileName = delFile_form.cleaned_data['FileName']    # 获取删除的文件名
            lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
            if lockbaseinfo:
                islock = lockbaseinfo[0].islock
                if islock:
                    delfile_message = "已锁库，禁止上传和删除！"
                else:
                    if os.path.exists(path+FileName):
                        os.remove(path+FileName)
                        delfile_message="【%s】 删除成功！！"%FileName
                    else:
                        delfile_message = "【%s】 文件不存在，删除失败！！" % FileName
            else:
                if os.path.exists(path + FileName):
                    os.remove(path + FileName)
                    delfile_message = "【%s】 删除成功！！" % FileName
                else:
                    delfile_message = "【%s】 文件不存在，删除失败！！" % FileName

        fileObjectList, dirObjectList= downloadFileInfo(path)

        delFile_form = DelFile()

        return render(request, 'software/uploadFile.html', locals())
    else:
        # return HttpResponse('<h4 style="color: red;font-weight: bold">删除文件后请勿刷新，回退一步或重新打开即可！</h4>')
        user_home = 'uploads/' + request.session['user_name'] + '/'
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下

        dirname = request.GET.get('dirname')

        if dirname:
            up_one_level_path = up_one_level(dirname)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'

        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]

            if request.session['user_name'] in versionManagerUsers:
                if len(dirname.split('/')) == 4:
                    domain_name = dirname.split('/')[2]
                    temp_domain_name = domain_name.split('（')[0]
                    file_path = dirname
                    try:
                        all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                           temp_domain_name, file_path)
                    except:
                        pass

            if request.session['user_name'] in versionManagerUsers:
                if len(dirname.split('/')) == 4:
                    print('******************** 不是空值 ********************')
                    domain_name = dirname.split('/')[2]
                    file_path = dirname
                    try:
                        all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                           domain_name, file_path)
                    except:
                        pass

            path = dirname + '/'
        # print('~~~~~~~~~~~~~~~dirname：', dirname)

        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        fileObjectList, dirObjectList = downloadFileInfo(path)

        delFile_form = DelFile()
        return render(request, 'software/uploadFile.html', locals())

def uploadFile(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(uploadFile.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【文件管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    path = 'uploads/' + request.session['user_name'] + '/'  # 上传文件路径，相对路径，在项目根目录下
    if not os.path.exists(path):  # 目录不存在则创建
        os.makedirs(path)

    user_management_config = getConfig('config/software_config/user_management_config.ini')
    # 版本管理用户,黑名单目录下不显示上传功能
    versionManagerUsers = user_management_config.get_value('user_list', 'black_user_list').split(',')

    # 用户家目录
    user_home ='uploads/' + request.session['user_name'] + '/'
    if request.session['user_name'] in versionManagerUsers:
        # print('登录的用户名是：', request.session['user_name'])
        shar_dir_list = []  # shar用户家目录的文件夹列表

        for user in versionManagerUsers:
            shar_dir_list.append('uploads/' + user + '/')

        for dir in os.listdir(user_home):
            if os.path.isdir(user_home + dir):
                shar_dir_list.append(user_home + dir + '/')
        # print('不在这些目录下展示上传功能：', shar_dir_list)

    delFile_form = DelFile()  # 宣染删除表格，即宣染删除功能的输入框

    dirname = request.GET.get('dirname')

    if dirname is not None:
        userRootPath = dirname.split('/')[1]
        # print('当前获取的用户家目录：', userRootPath)
        if request.session['user_name'] != userRootPath:
            return render(request, 'software/ERROR.html',locals())

        if dirname[-1] == '/':
                dirname = dirname[:-1]

        if request.session['user_name'] in versionManagerUsers:
            if len(dirname.split('/')) == 4:
                domain_name=dirname.split('/')[2]
                temp_domain_name=domain_name.split('（')[0]
                file_path=dirname
                try:
                    all_check_report_dict=match_productionMaterials(request.session['user_name'],temp_domain_name,file_path)
                except:
                    pass

        up_one_level_path = up_one_level(dirname)

        if os.path.isdir(dirname):
            path = dirname + '/'
            # print('=' * 50 + '获取到的绝对路径path：', path)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'
        else:
            # print('*' * 50 + '获取到的绝对路径：', dirname)
            return HttpResponse('<h4 style="color: red;font-weight: bold">访问错误,访问网页不存在！</h4>')
    else:
        dirname=path[:-1]

    fileObjectList, dirObjectList = downloadFileInfo(path)

    if request.method == 'POST':
        dirname = request.POST.get('dirname')
        # print('--------------------------获取到的目录-----------------------------')
        # print(dirname)
        # print('------------------------------------------------------------------')

        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]
            up_one_level_path = up_one_level(dirname)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'

            path=dirname+'/'
            # print('----------------------------当前路径-------------------------------')
            # print(path)
            # print('------------------------------------------------------------------')

        # file = request.FILES['file']  # 获取单个上传的文件对象，如果上传了多个，只取最后一个
        uploadFileList=request.FILES.getlist('file') # 获取所有上传的文件对象
        # print('************************所有上传的文件对象**************************')
        # print(uploadFileList)
        # print('******************************************************************')

        islock_base = request.POST.get('lock_base')  # 获取所有上传的文件对象
        # print('************************是否被锁库**************************')
        # print(islock_base)
        # print('******************************************************************')

        if islock_base:
            # print('islock_base')
            if islock_base == 'lock_base':
                lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
                if lockbaseinfo:
                    if lockbaseinfo[0].islock:
                        message='已经是被锁库状态！'
                    else:
                        lockbaseinfo[0].islock=True
                        lockbaseinfo[0].save()
                        message = '锁库成功！'
                else:
                    try:
                        # 添加锁库状态到数据库
                        newlockbaseinfo = LockBaseInfo.lockbase.create()
                        newlockbaseinfo.userName = request.session['user_name']
                        newlockbaseinfo.pathName = dirname
                        newlockbaseinfo.islock = True
                        newlockbaseinfo.save()
                        message = '锁库成功！'
                    except:
                        message = '锁库失败！'
            elif islock_base == 'unlock_base':
                try:
                    lockbaseinfo = LockBaseInfo.lockbase.get(pathName=dirname)
                    lockbaseinfo.islock = False
                    lockbaseinfo.save()
                    message = '解封库成功！'
                except:
                    message = '没有被锁库，不需要操作！'
            else:
                message = '操作失败！'
            # print(message)

        repeatFileList = [] # 记录重名的文件名
        upload_list_successful=[] # 记录上传成功的文件名
        uploadFailFiles = []    # 记录文件上传失败的，比如文件字过长
        repeatFileSum=0 # 重名文件的总个数

        lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
        if lockbaseinfo:
            islock = lockbaseinfo[0].islock
            if islock:
                message = "已锁库，禁止上传和删除！"
            else:
                if uploadFileList:
                    for file in uploadFileList:
                        # print(len(uploadFileList))
                        fileName=str(file) # 上传的文件名
                        # print("================== 文件名%s============="%fileName)
                        # print(path+fileName)

                        if os.path.exists(path+fileName):
                            repeatFileList.append(fileName) # 记录重名的文件名
                            continue
                            # return render(request, 'software/uploadFile.html', locals())
                        try:
                            with open(path + fileName, 'wb+') as destination:
                                for chunk in file.chunks():
                                    destination.write(chunk)
                            upload_list_successful.append(fileName) # 记录成功上传的文件名
                        except FileNotFoundError:
                            uploadFailFiles.append(fileName)

                    if len(upload_list_successful) != 0:
                        upload_successful_message = "上传成功列表如下："
                    if len(repeatFileList) != 0:
                        upload_failure_message = "【%d个文件重名，请重新命名再上传！】" % len(repeatFileList)
                    if len(uploadFailFiles) != 0:
                        uploadFailFiles_message = "【%d个文件名称过长，请重新命名再上传！】" % len(uploadFailFiles)
        else:
            if uploadFileList:
                for file in uploadFileList:
                    # print(len(uploadFileList))
                    fileName = str(file)  # 上传的文件名
                    # print("================== 文件名%s=============" % fileName)
                    # print(path + fileName)

                    if os.path.exists(path + fileName):
                        repeatFileList.append(fileName)  # 记录重名的文件名
                        continue
                        # return render(request, 'software/uploadFile.html', locals())
                    with open(path + fileName, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    upload_list_successful.append(fileName)  # 记录成功上传的文件名

                message = "%d个文件上传成功，%d个文件上传失败！！" % (len(upload_list_successful), len(repeatFileList)+len(uploadFailFiles))
                if len(upload_list_successful) != 0:
                    upload_successful_message = "上传成功列表如下："
                if len(repeatFileList) != 0:
                    upload_failure_message = "【%d个文件重名，请重新命名再上传！】" % len(repeatFileList)
                if len(uploadFailFiles) != 0:
                    uploadFailFiles_message = "【%d个文件名称过长，请重新命名再上传！】" % len(uploadFailFiles)
    else:
        message='温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        # print(message)

    lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
    if lockbaseinfo:
        islock = lockbaseinfo[0].islock
        # print('islock', islock)
    else:
        islock = False
    fileObjectList, dirObjectList = downloadFileInfo(path)
    user_home_path = "uploads/" + request.session['user_name']
    return render(request, 'software/uploadFile.html', locals())


def downloadFile(request, fileObject=None):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(downloadFile.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))


    try:
        if fileObject is None:
            # 获取上传文件路径和文件名，用于单个文件下载
            fileObject = request.POST.get('name')
            # 提取文件名
            tmp_list = fileObject.split('/')
            filename = tmp_list[-1]
        else:
            tmp_list = fileObject.split('/')
            filename = tmp_list[-1].split('_')[-1]
        # file = open(path+filename,'rb')
        # print('000000000000000000000000000000000')
        # print('文件名：',filename)
        # print('完整的路径：',fileObject)
        # print('000000000000000000000000000000000')
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())

    try:
        file = open(fileObject, 'rb')
    except:
        return HttpResponse('下载文件名有错，请联系管理员！  文件名：%s' % fileObject)
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


def newDirectory(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(newDirectory.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))


    try:
        dirname = request.GET.get('dirname')
        path = dirname
        # print('dirname GET方式传递过来的值:',dirname)
        up_one_level_path = up_one_level(path)
        # print('up_one_level_path：',up_one_level_path)
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())

    # 获取领域名
    domainName = dirname.split('/')[2]
    domainName = domainName.split('（')[0]

    config = getConfig('config/software_config/user_management_config.ini')
    user_list = config.get_value('user_list', 'black_user_list')
    user_list2 = user_list.split(',')

    # 如果是创建版本号目录则按版本目录规则创建目录
    if request.session['user_name'] in user_list2:
        # print(request.session['user_name'])
        if up_one_level_path == 'uploads':
            if not request.session.get('manager_islogin', None):
                message = "创建一级目录需要超级用户权限，您尚未登录超级用户，请先登录！！"
                return render(request, 'software/ERROR.html', locals())

        if path != 'uploads/' + request.session['user_name'] + '/1-版本检查单（收集）/':
            limit = True
            # print('limit：',limit)

        # 新增领域文件目录时，使用领域命名格式如:BCES-SECU（网银安全子系统）
        if path == 'uploads/' + request.session['user_name'] + '/':
            domain_naming = True
        # print('domain_naming：', domain_naming)

        for username in user_list2:
            if up_one_level_path == 'uploads/' + username:
                black_user = True
                # print('black_user：', black_user)
                break

    if request.method == "POST":
        dirname = request.POST.get('dirname')
        # print('dirname POST方式传递过来的值:', dirname)

        # 创建领域目录
        createDirectory_from = CreateDirectory(request.POST)
        if createDirectory_from.is_valid():
            engilistName = createDirectory_from.cleaned_data['englishName']
            chineseName = createDirectory_from.cleaned_data['chineseName']
            try:
                os.makedirs(dirname + engilistName + '（' + chineseName + '）')
                message = "%s 创建目录成功！" % (engilistName + '（' + chineseName + '）')
            except:
                message = "%s 创建目录失败，请检查目录是否已存在！" % (engilistName + '（' + chineseName + '）')
            # print(message)


        # 创建普通目录
        newDirectory_form = NewDirectory(request.POST)
        if newDirectory_form.is_valid():  # 如果有数据
            DirectoryName = newDirectory_form.cleaned_data['DirectoryName']  # 获取新建文件夹名
            try:
                os.makedirs(dirname + DirectoryName)
                message = "%s 创建目录成功！" % (DirectoryName)
            except:
                message = "%s 创建目录失败，请检查目录是否已存在！" % (DirectoryName)
            # print(message)

        # 创建版本目录
        CreateVersionDirectory_form = CreateVersionDirectory(request.POST)
        if CreateVersionDirectory_form.is_valid():  # 如果有数据
            VersionName = CreateVersionDirectory_form.cleaned_data['VersionName']  # 获取新建文件夹名,版本号
            Date = str(CreateVersionDirectory_form.cleaned_data['Date'])  # 获取投产日期

            name = VersionName[:len(domainName)]
            number = VersionName[len(domainName):]
            try:
                number_1, number_2, number_3 = number.split('.')
                # print('number_1,number_2,number_3: ',number_1,number_2,number_3)

                # 如果以下能转换成功说明全是数字，如果不能则报错
                number_1 = int(number_1)
                number_2 = int(number_2)
                number_3 = int(number_3)

                new_name = VersionName + '（' + Date + '）'
                new_name = new_name.replace(" ", "")

                if name == domainName:
                    try:
                        os.makedirs(dirname + new_name)
                        message = "%s 创建目录成功！" % (new_name)
                    except:
                        message = "%s 创建目录失败，请检查目录是否已存在！" % (new_name)
                else:
                    message = "%s 创建目录失败，目录格式错误！！" % (new_name)
            except:
                message = "%s 创建目录失败，目录格式错误！！" % (VersionName + '（' + Date + '）')
            # print(message)

    createDirectory_from = CreateDirectory()
    newDirectory_form = NewDirectory()
    CreateVersionDirectory_form = CreateVersionDirectory()
    return render(request, 'software/newDirectory.html', locals())


def rename_directory(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(rename_directory.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您尚未登录超级用户，请先登录！！"
        return render(request, 'software/index.html', locals())

    try:
        # 获取当前函数名
        function_name = sys._getframe().f_code.co_name

        dirname = request.GET.get('dirname')
        path = dirname
        # print('dirname GET方式传递过来的值:',dirname)
        up_one_level_path = up_one_level(path)
        up_two_level_path = up_one_level(up_one_level_path)

        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]

        old_dir_name = dirname.split('/')[-1]
        # print('旧目录名：',old_dir_name)
        # print('上一级目录名：',up_one_level_path)
        # print('上二级目录名：',up_two_level_path)

        # 获取领域名
        domainName = dirname.split('/')[2]
        domainName = domainName.split('（')[0]

        config = getConfig('config/software_config/user_management_config.ini')
        user_list = config.get_value('user_list', 'black_user_list')
        user_list2 = user_list.split(',')

        # 如果是创建版本号目录则按版本目录规则创建目录
        if request.session['user_name'] in user_list2:
            # print(request.session['user_name'])
            if up_one_level_path != 'uploads/' + request.session['user_name'] + '/1-版本检查单（收集）':
                limit = True

            if up_one_level_path == 'uploads/' + request.session['user_name']:
                domain_naming = True
                # print('domain_naming：', domain_naming)

            for username in user_list2:
                if up_two_level_path == 'uploads/' + username:
                    black_user = True
                    break
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())

    if request.method == "POST":
        dirname = request.POST.get('dirname')
        # print('dirname POST方式传递过来的值:', dirname)

        createDirectory_from = CreateDirectory(request.POST)
        if createDirectory_from.is_valid():
            engilistName = createDirectory_from.cleaned_data['englishName']
            chineseName = createDirectory_from.cleaned_data['chineseName']
            try:
                os.rename(up_one_level_path + '/' + old_dir_name, up_one_level_path + '/' + engilistName + '（' + chineseName + '）')
                message = "%s 修改目录成功！" % (engilistName + '（' + chineseName + '）')
            except:
                message = "%s 修改目录失败，请检查目录是否已存在！" % (engilistName + '（' + chineseName + '）')
            # print(message)

        newDirectory_form = NewDirectory(request.POST)
        if newDirectory_form.is_valid():  # 如果有数据
            DirectoryName = newDirectory_form.cleaned_data['DirectoryName']  # 获取新建文件夹名
            # print('获取新的目录名：',DirectoryName)
            # print('旧的完整名：',up_one_level_path+'/'+old_dir_name)
            # print('新的完整名：',up_one_level_path+'/'+DirectoryName)
            try:
                os.rename(up_one_level_path + '/' + old_dir_name, up_one_level_path + '/' + DirectoryName)
                message = "%s 修改目录成功！" % (DirectoryName)
            except:
                message = "%s 修改目录失败，请检查目录是否已存在！" % (DirectoryName)
            # print(message)

        CreateVersionDirectory_form = CreateVersionDirectory(request.POST)
        if CreateVersionDirectory_form.is_valid():  # 如果有数据
            VersionName = CreateVersionDirectory_form.cleaned_data['VersionName']  # 获取新建文件夹名,版本号
            Date = str(CreateVersionDirectory_form.cleaned_data['Date'])  # 获取投产日期

            name = VersionName[:len(domainName)]
            number = VersionName[len(domainName):]
            try:
                number_1, number_2, number_3 = number.split('.')
                # print('number_1,number_2,number_3: ',number_1,number_2,number_3)

                # 如果以下能转换成功说明全是数字，如果不能则报错
                number_1 = int(number_1)
                number_2 = int(number_2)
                number_3 = int(number_3)

                new_name = VersionName + '（' + Date + '）'
                new_name = new_name.replace(" ", "")

                if name == domainName:
                    try:
                        os.rename(up_one_level_path + '/' + old_dir_name, up_one_level_path + '/' + new_name)
                        message = "%s 修改成功！" % (new_name)
                    except:
                        message = "%s 修改失败，请检查目录是否已存在！" % (new_name)
                else:
                    message = "%s 修改失败，目录格式错误！！" % (new_name)
            except:
                message = "%s 修改失败，目录格式错误！！" % (VersionName + '（' + Date + '）')
            # print(message)

    createDirectory_from = CreateDirectory()
    newDirectory_form = NewDirectory()
    CreateVersionDirectory_form = CreateVersionDirectory()
    return render(request, 'software/rename_directory.html', locals())


def mycopy(src_file, dst_file):
    """此函数的功以实现复制文件
    src_file : 源文件名
    dst_file : 目标文件名
    """
    try:
        with open(src_file, "rb") as fr, open(dst_file, 'wb') as fw:
            while True:
                data = fr.read(4096)
                if not data:
                    break
                fw.write(data)
    except OSError:
        print("打开读文件失败")
        return False
    except:
        print("读写中断了！")
    return True


# def allFileDownload(request):
#     '''使用临时文件方法，临时文件在文件关闭时会被自动删除。
#         测试了，windowns并被没有删除，未知原因。
#     '''
#     # 获取文件原路径
#     source_dir = request.GET.get('source_dir')
#     print('source_dir GET方式传递过来的值:', source_dir)
#     if source_dir[-1] == '/':
#         source_dir = source_dir[:-1]
#     # 生成临时目录作为打zip包目录，用户下载完成后会自动删除
#     output_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")+'_'+source_dir.split('/')[-1]+'.zip'
#     filename = output_filename.split('_')[-1]
#     print('zip包名：', output_filename)
#     output_dir = 'uploads/'+ 'temp'
#     print('存放zip包临时目录：', output_dir)
#     # 临时目录不存在则创建
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     # 打包zip包
#     make_zip(source_dir, output_dir, output_filename)
#     print('打包完成！！！')
#     newfile = NamedTemporaryFile(suffix='.django.tmp',dir=output_dir)
#     print('NamedTemporaryFile临时文件名：',newfile.name)
#     mycopy(output_dir+'/'+output_filename,newfile.name)
#     print('将数据拷贝到临时文件完成：',newfile.name)
#     try:
#         os.remove(output_dir+'/'+output_filename)
#     except:
#         print('删除临时zip包失败！',output_dir+'/'+output_filename)
#
#     return downloadFile(request,newfile.name,filename)


def allFileDownload(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(allFileDownload.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    try:
        clientIP = request.META['REMOTE_ADDR']
        webName = str(versionManagerIndex.__name__)
        logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
        # 获取文件原路径
        source_dir = request.GET.get('source_dir')
        # print('source_dir GET方式传递过来的值:', source_dir)
        if source_dir[-1] == '/':
            source_dir = source_dir[:-1]
            # 生成临时目录作为打zip包目录，用户下载完成后会自动删除
        output_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '_' + source_dir.split('/')[-1] + '.zip'
        # print('目录作为打zip包名：', output_filename)
        output_dir = 'uploads/' + 'temp'
        # print('存放zip包临时目录：', output_dir)
        # 临时目录不存在则创建
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # 打包zip包
        make_zip(source_dir, output_dir, output_filename)
        # print('打包完成！！！')
        return downloadFile(request, output_dir + '/' + output_filename)
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())


def versionManagerIndex(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/versionManagerIndex.html')


def T8_index(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(T8_index.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/T8_index.html')


def CDNofflink(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(CDNofflink.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/CDNofflink.html')


def tdc(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(tdc.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/tdc.html')


def extranetAddress(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(extranetAddress.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/extranetAddress.html')


def setServerDate(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(setServerDate.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【服务器时间管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您不是超级用户，无法使用【服务器时间管理】功能！！"
        return render(request, 'software/index.html', locals())

    # 获取数据库里的数据
    timersList = TimingData.timers.all()
    for timer in timersList:
        print('===================')
        print(timer.pk)
        print(timer.clientJobID)
        print(timer.execTime)
        print(timer.setTime)
        print(timer.serverIP)
        print('===================')

    message = '添加定时任务'
    if request.method == "POST":
        date_form = DateForm(request.POST)  # DateForm 为models里对应的类名
        print(date_form)
        if date_form.is_valid():  # 如果有数据
            Datetime = date_form.cleaned_data['Datetime']
            ServerDatetime = date_form.cleaned_data['ServerDatetime']  # 获取日期和时间
            ServerIP = date_form.cleaned_data['ServerIP']  # 获取IP
            MyJobID = request.session['user_name'] + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            print(ServerIP)
            print(Datetime.strftime("%Y-%m-%d %H:%M:%S"))
            print(ServerDatetime.strftime("%Y-%m-%d %H:%M:%S"))
            print(MyJobID)

            # 如果提示某字段不能为空，请到数据库手工修改可以为空值，即把：不是null 的勾去掉
            print('创建数据库表实例开始----------------------------')
            newTimer = TimingData.timers.create()
            print('添加执行时间----------------------------')
            newTimer.execTime = Datetime
            print('添加设置----------------------------')
            newTimer.setTime = ServerDatetime
            print('添加服务器IP----------------------------')
            newTimer.serverIP = ServerIP
            print('添加线程my_job_id----------------------------')
            newTimer.clientJobID = MyJobID
            print('保存到数据库----------------------------')
            newTimer.save()

            # 设置服务器时间
            def timerHelper(MyJobID):
                __username = 'root'
                __password = '123456'
                class TheServerHelper():
                    """初始化函数构造
                        其中commond作为执行的语句"""
                    def __init__(self, clientIP, username, password, date, port=22):
                        self.serverIP = '192.168.43.100'
                        self.clientIP = clientIP
                        self.username = username
                        self.password = password
                        self.port = port
                        self.date = date
                    # SSH连接服务器，用于命令执行
                    def ssh_connectionServer(self):
                        import paramiko
                        print(self.serverIP)
                        print(self.clientIP)
                        print(self.username)
                        print(self.password)
                        print(self.port)
                        set_time = 'date -s "%s"' % (self.date)
                        print(set_time)
                        cmds = ['export LANG=zh_CN.UTF-8', 'echo $LANG', 'pwd', 'ls -lh', 'hostname -i', 'date']
                        cmds.insert(0, set_time)

                        try:
                            print('创建SSH对象--------')
                            # 创建SSH对象
                            sf = paramiko.SSHClient()
                            # 允许连接不在know_hosts文件中的主机
                            sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            print('开始连接堡垒机服务器：%s' % self.serverIP)
                            # 连接服务器
                            sf.connect(hostname=self.serverIP, port=self.port, username=self.username,
                                       password=self.password)
                            print('连接堡垒机服务器成功！')

                            print('激活连接的终端！')
                            channel = sf.invoke_shell()
                            print('设置读、写操作超时时间')
                            channel.settimeout(10)
                            print('发送命令行：%s' % cmds)
                            time.sleep(0.5)

                            for command in cmds:
                                channel.send(command + '\n')
                                time.sleep(0.5)
                                try:
                                    command_res = channel.recv(65533).decode('utf-8')
                                    # print('-' * 30)
                                    # print(command_res)
                                    # print('-' * 30)
                                except Exception as e:
                                    print('*' * 30)
                                    print(e)
                                    print('*' * 30)
                                    break
                            channel.close()
                            sf.close()
                        except Exception as e:
                            print('=' * 30)
                            print(e)
                            print('=' * 30)
                        return True

                        #     # 注意：依次执行多条命令时，命令之间用分号隔开
                        #     stdin, stdout, stderr = sf.exec_command(set_time)
                        #     result = stdout.read().decode('utf-8')
                        #     print("命令执行成功！\n结果如下：\n%s" % result)
                        #     time.sleep(3)
                        #     stdin, stdout, stderr = sf.exec_command('date')
                        #     result = stdout.read().decode('utf-8')
                        #     print("命令执行成功！\n结果如下：\n%s" % result)
                        # except:
                        #     print("连接服务器：" + self.serverIP + " 失败了!")
                        #     return False

                # 获取数据库定时任务的信息
                timerInfo = TimingData.timers.all()  # 获取所有对象显示到页面
                for timer in timerInfo:
                    clientJobID = timer.clientJobID
                    if clientJobID == MyJobID:
                        jobisDelete = timer.isDelete
                        serverIP = timer.serverIP
                        setTime = timer.setTime.strftime("%Y-%m-%d %H:%M:%S")  # 获取日期 如：2020-3-23 12:11:00
                        print(clientJobID, jobisDelete)

                        # 判断任务是否被删除了
                        if jobisDelete == 0:
                            # 执行任务
                            serverHelper = TheServerHelper(serverIP, __username, __password, setTime, port=22)
                            serverHelper.ssh_connectionServer()
                            timerInfo = TimingData.timers.get(clientJobID=MyJobID)
                            timerInfo.delete()
                        break

            def createTimedTasks(MyJobID, year, month, day, hour, minute, second):
                schedulers = BackgroundScheduler()
                # cron定时调度（某一定时时刻执行），表示2017年3月22日17时19分07秒执行该程序
                schedulers.add_job(timerHelper, 'cron', id=MyJobID,
                                   year=year, month=month, day=day, hour=hour, minute=minute, second=second, args=[MyJobID])

                # interval间隔调度，4个参数分别为：函数、类型、线程id、执行时间间隔
                # sched.add_job(job, 'interval', id=job_id, seconds=1)

                # date 定时调度（作业只会执行一次）
                # The job will be executed on November 6th, 2009 at 16:30:05
                # sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
                schedulers.start()
            message = '添加定时任务成功！！'

            exec_year = Datetime.strftime('%Y')
            exec_month = Datetime.strftime('%m')
            exec_day = Datetime.strftime('%d')
            exec_hour = Datetime.strftime('%H')
            exec_minute = Datetime.strftime('%M')
            exec_second = Datetime.strftime('%S')
            createTimedTasks(MyJobID, exec_year, exec_month, exec_day, exec_hour, exec_minute, exec_second)

    timersList = TimingData.timers.all()
    date_form = DateForm()
    deldate_form = DelForm()
    return render(request, 'software/setServerDate.html', locals())


def delServerDate(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(delServerDate.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if request.method == "POST":
        try:
            clientJobID = request.POST.get('clientJobID')
            # print(clientJobID)
            if clientJobID is not None:
                timerInfo = TimingData.timers.get(clientJobID=clientJobID)
                # print(timerInfo)
                timerInfo.delete()
                successful_message = "【%s】删除成功！！" % clientJobID
            else:
                deldate_form = DelForm(request.POST)  # DateForm 为models里对应的类名,作为date_form.is_valid()铺垫
                if deldate_form.is_valid():  # 如果有数据，models里对应的类名,类里面有几个变量就获取几个，如果有一个报错则为空
                    MyJobID = deldate_form.cleaned_data['MyJobID']  # 获取线程ID
                    failure_msg = "【%s】删除失败！！" % MyJobID
                    timerInfo = TimingData.timers.get(clientJobID=MyJobID)
                    if MyJobID == timerInfo:
                        timerInfo.delete()
                        successful_message = "【%s】删除成功！！" % MyJobID
                        # print(successful_message)
        except:
            pass
    message = '添加定时任务'
    timersList = TimingData.timers.all()
    date_form = DateForm()
    deldate_form = DelForm()
    return render(request, 'software/setServerDate.html', locals())


def productionMaterials(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(productionMaterials.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【投产材料管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    user_management_config = getConfig('config/software_config/user_management_config.ini')
    # 访问此功能的白名单用户, 白名单可访问投产材料管理页面
    allow_users = user_management_config.get_value('user_list', 'allow_users_list').split(',')

    user_dir_list = []
    if request.session['user_name'] in allow_users:
        user_path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        for dir in os.listdir(user_path):
            # print(dir)
            # print(user_path+dir)
            if os.path.isdir(user_path + dir):
                user_dir_list.append(dir)
        user_dir_list = sorted(user_dir_list)
        # print('用户下所有目录名：',user_dir_list) #['BCOS-MNGT', 'BRON', 'BRON-CLSS', 'BRON-CRMP', 'BRON-LPSS']

        if request.method == "GET":
            dirname = request.GET.get('domain')
            # print('GET方式获取到的dirname：',dirname)

            if dirname:
                version_dir_list = []
                version_path = 'uploads/' + request.session['user_name'] + '/' + dirname + '/'
                # print('当前路径：',version_path)
                for dir in os.listdir(version_path):
                    # print('当前目录：',dir)
                    if os.path.isdir(version_path + dir):
                        version_dir_list.append(dir)
                version_dir_list = sorted(version_dir_list)
                # print('当前所有版本：',version_dir_list)
        if request.method == "POST":
            # 获取目录，如：BCOS-MNGT（渠道作业管理系统）/BCOS-MNGT1.1.0（2020-05-10）
            version_name = request.POST.get('version_name')
            # print('获取目录version_name：',version_name)
            # 获取领域名
            domain_name = version_name.split('/')[0]
            # print('获取领域名domain_name：',domain_name)
            temp_domain_name = domain_name.split('（')[0]
            # print('temp_domain_name：',temp_domain_name)
            # 获取完整路径，如：uploads/shar/BCOS-MNGT（渠道作业管理系统）/BCOS-MNGT1.1.0（2020-05-10）
            file_path = user_path + version_name
            # print('获取完整路径file_path：',file_path)
            # 获取文件目录名,如：BCOS-MNT1.1.0（2020-05-14）
            domain_path = version_name.split('/')[1]
            # print('获取文件目录名domain_path：',domain_path)
            # # 获取领域+版本号，如：BCOS-MNT1.1.0
            # dir_name = version_name.split('（')[0]
            # # 大升级号,如BCOS-MNGT1 ;常规号,如1; 紧急号,如0
            # dig_upgrade_number,conventional_number, emergency_number = dir_name.split('.')
            # # 把字母和数据分离，并取字符串末的数字，如BCOS-MNGT1，取的值为:1
            # span=re.search('\d{1,2}$',dig_upgrade_number)
            # dig_upgrade_number=dig_upgrade_number[span.start():span.end()]
            # print('大升级号:',dig_upgrade_number )
            # print('常规号:',conventional_number )
            # print('紧急号:',emergency_number )
            #
            # version=dig_upgrade_number+'.'+conventional_number+'.'+emergency_number
            # print('版本号为：',version)
            # print('-------------------test1---------------------------')
            # print("当前目录名domain_name：", domain_name)
            # print("领域名temp_domain_name：", temp_domain_name)
            # print("文件路径file_path：",file_path)
            # print('-------------------test1---------------------------')

            try:
                one_check_report_dict = match_productionMaterials(request.session['user_name'], temp_domain_name, file_path)
                print('查询的领域收集投产材料情况：', one_check_report_dict)
            except:
                print('查询单个领域收集投产材料情况失败，配置中没有对应领域数据！')

        # 投产日期集合
        date_list = []
        # 获取前端传过来的日期，只查询筛选的日期版本
        checkoutDate = request.GET.get('checkoutDate')
        # print('checkoutDate',checkoutDate)

        # 存放所有领域版本投产资料收集情况
        all_check_report_list = []
        # 遍历用户下面所有领域，并检查投产材料收集情况
        for domain in user_dir_list:
            temp_domain_name = domain.split('（')[0]
            # print('temp_domain_name: ',temp_domain_name)
            for dir in os.listdir(user_path + domain):  # 获取用户下所有领域目录和文件
                # print('dir: ',dir)
                # 获取所有投产日期
                try:
                    temp_date = dir.split('（')[1]
                    temp_date = temp_date.split('）')[0]
                    if temp_date not in date_list:
                        date_list.append(temp_date)  # 给到前端显示

                    # 只查询筛选的日期版本
                    if checkoutDate:
                        if checkoutDate in dir:
                            print('只查询筛选的日期版本checkoutDate:%s, temp_date:%s, dir:%s' % (checkoutDate, temp_date, dir))
                        elif checkoutDate == "所有版本":
                            print('查询所有日期版本')
                        else:
                            # print('checkoutDate: ',checkoutDate)
                            continue
                    else:
                        continue
                except:
                    # print('目录格式不对！！')
                    # 只查询筛选的日期版本
                    if checkoutDate:
                        print('只查询筛选的日期版本', checkoutDate)
                finally:
                    # print('date_list: ',date_list)
                    pass

                # print('=======================*********************++++++++++++++++++++++++++++')
                if os.path.isdir(user_path + domain + '/' + dir):
                    # print('当前获取的文件完整路径：', user_path + domain + '/' + dir)
                    #
                    # print('-------------------test2---------------------------')
                    # print("领域名temp_domain_name：", temp_domain_name)
                    # print("文件路径file_path：", user_path+domain+'/'+dir)
                    # print('-------------------test2---------------------------')

                    try:
                        # 存放单个领域版本投产资料收集情况
                        all_check_report_dict = match_productionMaterials(request.session['user_name'],
                                                                          temp_domain_name,
                                                                          user_path + domain + '/' + dir)
                        # print('所有领域版本投产资料收集情况：', all_check_report_dict)
                    except:
                        # print('所有领域版本投产资料收集情况，配置中没有对应领域数据！')
                        continue

                    all_check_report_list.append(all_check_report_dict)

        date_list = sorted(date_list, reverse=True)
        # print('当前所有投产日期：',date_list)
        # 读配置
        report_config = configparser.ConfigParser()
        report_config.read('config/software_config/report_check_list_config.ini', encoding='UTF-8')
        # 获取所有检查报告，不分前后端
        table_title = report_config.get('report_check_list', 'ALL')
        # 去空格
        table_title = table_title.strip()
        # 把字符串(配置)转换为列表
        table_title = table_title.split(',')
        table_title.insert(0, '版本号')
        return render(request, 'software/productionMaterials.html', locals())
    else:
        return render(request, 'software/ERROR.html', locals())


# def unblockedVersion(request):
#     clientIP = request.META['REMOTE_ADDR']
#     webName = str(unblockedVersion.__name__)
#     logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
#
#     if not request.session.get('is_login', None):
#         uploadFile_message = "您尚未登录，使用【解封版信息收集】请先登录！！"
#         return render(request, 'software/index.html', locals())
#
#     if request.method == "POST":
#         if request.POST.get('options') == "insert":
#             newUnblocked_version = UnblockedVersionInfo.unblockedversion.create()
#             newUnblocked_version.username = request.session['user_name']
#             newUnblocked_version.month = request.POST.get('month')
#             newUnblocked_version.team = request.POST.get('team')
#             newUnblocked_version.version_number = request.POST.get('version_number')
#             newUnblocked_version.subsystem = request.POST.get('subsystem')
#             newUnblocked_version.version_name = request.POST.get('version_name')
#             newUnblocked_version.content = request.POST.get('content')
#             newUnblocked_version.version_compiler = request.POST.get('version_compiler')
#             newUnblocked_version.version_leader = request.POST.get('version_leader')
#             newUnblocked_version.test_leader = request.POST.get('test_leader')
#             newUnblocked_version.development_team = request.POST.get('development_team')
#             newUnblocked_version.version_type = request.POST.get('version_type')
#             newUnblocked_version.unblocked_datetime = request.POST.get('unblocked_datetime')
#             newUnblocked_version.blocked_datetime = request.POST.get('blocked_datetime')
#             newUnblocked_version.unblocked_type = request.POST.get('unblocked_type')
#             newUnblocked_version.unblocked_reason = request.POST.get('unblocked_reason')
#             newUnblocked_version.save()
#         elif request.POST.get('options') == "delete":
#             if not request.session.get('manager_islogin', None):
#                 message = "您尚未登录超级用户，请先登录！！"
#             else:
#                 username = request.session['user_name']
#                 id = request.POST.get('id')
#                 try:
#                     getUnblocked_version_list = UnblockedVersionInfo.unblockedversion.filter(username=username, id=id)
#                 except Exception as e:
#                     logging.info("ERROR：来自：%s, " % e)
#                     getUnblocked_version_list = None
#                     message = "删除数据失败，获取不到对应的数据！"
#
#                 # 删除数据
#                 if getUnblocked_version_list:
#                     for unblocked_version in getUnblocked_version_list:
#                         unblocked_version.delete()
#                         message = "删除数据成功！"
#         else:
#             message = "提交信息有误，请刷新页面重新提交！"
#
#     # @register.filter
#     # def get_range(value):
#     #     return range(value)
#
#     # 从数据库中查询当前登录用户的解封版所收集的信息
#     unblocked_versionInfo_list = UnblockedVersionInfo.unblockedversion.filter(
#         username=request.session['user_name']).order_by('-id')
#     return render(request, 'software/unblockedVersion.html', locals())


def unblockedVersion(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(unblockedVersion.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【解封版信息收集】请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == "POST":
        if request.POST.get('options') == "insert":
            newUnblocked_version = NewUnblockedVersionInfo.newunblockedversion.create()
            newUnblocked_version.username = request.session['user_name']
            newUnblocked_version.month = request.POST.get('month')
            newUnblocked_version.team = request.POST.get('team')
            newUnblocked_version.version_name = request.POST.get('version_name')
            newUnblocked_version.subsystem = request.POST.get('subsystem')
            newUnblocked_version.content = request.POST.get('content')
            newUnblocked_version.version_manager = request.POST.get('version_manager')
            newUnblocked_version.version_leader = request.POST.get('version_leader')
            newUnblocked_version.test_leader = request.POST.get('test_leader')
            newUnblocked_version.version_type = request.POST.get('version_type')
            newUnblocked_version.unblocked_datetime = request.POST.get('unblocked_datetime')
            newUnblocked_version.blocked_datetime = request.POST.get('blocked_datetime')
            newUnblocked_version.unblocked_type = request.POST.get('unblocked_type')
            newUnblocked_version.unblocked_reason = request.POST.get('unblocked_reason')
            newUnblocked_version.remark = request.POST.get('remark')
            newUnblocked_version.save()
        elif request.POST.get('options') == "delete":
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                username = request.session['user_name']
                id = request.POST.get('id')
                try:
                    getUnblocked_version_list = NewUnblockedVersionInfo.newunblockedversion.filter(username=username, id=id)
                except Exception as e:
                    logging.info("ERROR：来自：%s, " % e)
                    getUnblocked_version_list = None
                    message = "删除数据失败，获取不到对应的数据！"

                    # 删除数据
                if getUnblocked_version_list:
                    for unblocked_version in getUnblocked_version_list:
                        unblocked_version.delete()
                        message = "删除数据成功！"
        elif request.POST.get('options') == "downloadFile":
            if not request.session.get('manager_islogin', None) and request.POST.get('user') == "all":
                message = "您尚未登录超级用户，请先登录！！"
            else:
                try:
                    userList = []
                    monthList = []
                    teamList = []
                    version_nameList = []
                    subsystemList = []
                    contentList = []
                    version_managerList = []
                    version_leaderList = []
                    test_leaderList = []
                    version_typeList = []
                    unblocked_datetimeList = []
                    blocked_datetimeLIst = []
                    unblocked_typeList = []
                    unblocked_reasonList = []
                    remarkList = []

                    monthsList = request.POST.getlist('month')

                    # if request.POST.get('user') == "all":
                    #     # 获取已有数据
                    #     unblocked_versionInfo = NewUnblockedVersionInfo.newunblockedversion.filter(isDelete=0).order_by(
                    #         'username', '-id')
                    # else:
                    #     unblocked_versionInfo = NewUnblockedVersionInfo.newunblockedversion.filter(isDelete=0, username=
                    #     request.session['user_name']).order_by('-id')
                    #
                    # for versionInfo in unblocked_versionInfo:
                    #     if versionInfo.month in monthsList:
                    #         userList.append(versionInfo.username)
                    #         monthList.append(versionInfo.month)
                    #         teamList.append(versionInfo.team)
                    #         version_nameList.append(versionInfo.version_name)
                    #         subsystemList.append(versionInfo.subsystem)
                    #         contentList.append(versionInfo.content)
                    #         version_managerList.append(versionInfo.version_manager)
                    #         version_leaderList.append(versionInfo.version_leader)
                    #         test_leaderList.append(versionInfo.test_leader)
                    #         version_typeList.append(versionInfo.version_type)
                    #         unblocked_datetimeList.append(versionInfo.unblocked_datetime)
                    #         blocked_datetimeLIst.append(versionInfo.blocked_datetime)
                    #         unblocked_typeList.append(versionInfo.unblocked_type)
                    #         unblocked_reasonList.append(versionInfo.unblocked_reason)
                    #         remarkList.append(versionInfo.remark)

                    q1 = Q()
                    q1.connector = 'OR'
                    for mon in monthsList:
                        q1.children.append(('month', mon))

                    q2 = Q()
                    q2.connector = 'OR'
                    q2.children.append(('isDelete', 0))

                    con = Q()
                    con.add(q1, 'AND')
                    con.add(q2, 'AND')

                    if request.POST.get('user') == "all":
                        # 获取已有数据
                        unblocked_versionInfo = NewUnblockedVersionInfo.newunblockedversion.filter(con).order_by(
                            'username', '-id')
                    else:
                        q3 = Q()
                        q3.connector = 'OR'
                        q3.children.append(('username', request.session['user_name']))
                        con.add(q3, 'AND'  )
                        unblocked_versionInfo = NewUnblockedVersionInfo.newunblockedversion.filter(con).order_by('-id')

                    for versionInfo in unblocked_versionInfo:
                        userList.append(versionInfo.username)
                        monthList.append(versionInfo.month)
                        teamList.append(versionInfo.team)
                        version_nameList.append(versionInfo.version_name)
                        subsystemList.append(versionInfo.subsystem)
                        contentList.append(versionInfo.content)
                        version_managerList.append(versionInfo.version_manager)
                        version_leaderList.append(versionInfo.version_leader)
                        test_leaderList.append(versionInfo.test_leader)
                        version_typeList.append(versionInfo.version_type)
                        unblocked_datetimeList.append(versionInfo.unblocked_datetime)
                        blocked_datetimeLIst.append(versionInfo.blocked_datetime)
                        unblocked_typeList.append(versionInfo.unblocked_type)
                        unblocked_reasonList.append(versionInfo.unblocked_reason)
                        remarkList.append(versionInfo.remark)


                    data = {'小组': userList, '月份': monthList, '领域': teamList, '版本名称': version_nameList,
                            '子系统名称': subsystemList,
                            '版本需求': contentList, '版本经理': version_managerList, '开发负责人': version_leaderList,
                            '测试负责人': test_leaderList, '版本类型': version_typeList, '解封开始时间': unblocked_datetimeList,
                            '封版时间': blocked_datetimeLIst, '解封版类别': unblocked_typeList,
                            '解封版说明及根因分析': unblocked_reasonList, '备注': remarkList}

                    path = 'uploads/' + 'temp' + '/'
                    tempFileName = 'unblockedVersionInfo' + '_' + request.session[
                        'user_name'] + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.xlsx'
                    outputFileName = 'unblockedVersionInfo.xlsx'

                    import pandas as pd
                    df = pd.DataFrame(data)
                    df.to_excel(path + tempFileName, index=False)

                    try:
                        file = open(path + tempFileName, 'rb')
                    except:
                        return HttpResponse('下载文件名有错，请联系管理员！  文件名：%s' % outputFileName)

                    response = FileResponse(file)
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
                        escape_uri_path(outputFileName))
                    return response

                except Exception as e:
                    print(e)
                    unblocked_versionInfo = None
        else:
            message = "提交信息有误，请刷新页面重新提交！"

    # @register.filter
    # def get_range(value):
    #     return range(value)

    # 从数据库中查询当前登录用户的解封版所收集的信息
    unblocked_versionInfo_list = NewUnblockedVersionInfo.newunblockedversion.filter(username=request.session['user_name'],isDelete=0).order_by('-id')
    return render(request, 'software/unblockedVersion.html', locals())


def modifySuperPWD(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(modifySuperPWD.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    # 修改二级密码
    if not request.session.get('is_login', None):
        return HttpResponse('<h4 style="color: red;font-weight: bold">您尚未登录普通用户，请先登录！！</h4>')

    modifyPassword = ModifySuperPWDForm()
    message = "超级用户密码修改"

    if request.method == "POST":
        username = request.session['user_name']
        # 从数据库获取用户对象信息
        managers = ManagerDate.managers.get(user=request.session['user_name'])

        passwd_from = ModifySuperPWDForm(request.POST)
        if passwd_from.is_valid():
            print(passwd_from.cleaned_data['password'])
            print(passwd_from.cleaned_data['password1'])
            print(passwd_from.cleaned_data['password2'])
            if passwd_from.cleaned_data['password1'] != passwd_from.cleaned_data['password2']:
                message = "输入新密码不一致！"
                return render(request, 'software/modifySuperPWD.html', locals())

            if managers.password == passwd_from.cleaned_data['password']:
                managers.password = passwd_from.cleaned_data['password1']
                managers.save()
                message = "修改成功"
            else:
                message = "原密码错误！"
                return render(request, 'software/modifySuperPWD.html', locals())

    return render(request, 'software/modifySuperPWD.html', locals())


# 获取gitlab分支commits中的SR号
class request_gitlab_api(object):
    def __init__(self, project_id, service_name, private_token):
        '''
        :param project_id: gitlab项目ID
        :param service_name: 接口名称
        :param private_token: 访问令牌
        '''
        self.project_id = project_id
        self.service_name = service_name
        self.private_token = private_token
        self.url = "http://gitlab.pab.com.cn/api/v4/projects/%s%s" % (project_id, service_name)
        print(self.url)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Private-Token': private_token
        }

    def get_gitlab_branch(self):
        '''获取项目下所有分支'''
        barnch_list_temp = []  # 存储所有分支
        barnch_list = []  # 存储所有有效的分支，已去除没有用的分支
        message=""

        page = 0
        while True:
            page += 1
            # parms_dict = {"search":"^Release_","per_page": 100, "page": page}
            parms_dict = {"per_page": 100, "page": page}
            r = requests.get(url=self.url, headers=self.headers, params=parms_dict)
            # print(r.json())
            if r.status_code == 200:
                r_list = r.json()  # 访问成功则返回为列表
                if r_list:
                    for branch_info in r_list:
                        barnch_list_temp.append(branch_info['name']) # 提取每个分支的名称
                else:
                    break
            else:
                # 访问失败则返回为字典
                message=r.json()["message"]
                break

        if barnch_list_temp:
            for barnch in barnch_list_temp:
                # 筛选有效的分支
                m = re.findall('^Release_|^master$|^main$', barnch, re.M | re.I | re.S)
                if m:
                    barnch_list.append(barnch)
            barnch_list = barnch_list[::-1]  # 按字母倒序排列

        data = {"barnch_list": barnch_list}
        foo = {"status_code": r.status_code, "data": data, "message": message}
        return json.dumps(foo, sort_keys=True, indent=4)

    def deploy_go_by_time(self, which_branch, date):
        '''
        :param which_branch: 分支名
        :param since: Only commits after or on this date will be returned in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ
        :return:
        '''

        # 计算指定时间的前N天的时间戳
        def get_days_time(date, n):
            the_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            pre_date = the_date - datetime.timedelta(days=n)
            pre_date = pre_date.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转换为指定的显示格式
            pre_time = time.strptime(pre_date, "%Y-%m-%d %H:%M:%S")  # 将时间转化为数组形式
            pre_stamp = int(time.mktime(pre_time))  # 将时间转化为时间戳形式
            # print(pre_stamp)
            return pre_stamp

        # 因为gitlab获取时间有差异，获取SR取提前1天
        timeStamp = get_days_time(date, 1)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
        # print("gitlab查询时间：",otherStyleTime)

        all_sr_list = []  # 存放commits里面的所有SR号
        page = 0
        while True:
            page += 1
            parms_dict = {"ref_name": which_branch, "since": otherStyleTime, "per_page": 100, "page": page}
            r = requests.get(url=self.url, headers=self.headers, params=parms_dict).text
            r_list = json.loads(r)
            # print('r_list: ',r_list)
            # logging.info(("INFO：r_list：%s") % (r_list))
            if len(r_list) == 0:
                break
            elif isinstance(r_list, dict):  # 如果是字典，可能是报错了，如：{'message': '404 Project Not Found'}
                break
            for commit in r_list:  # 获取每一个commit中的title信息
                # logging.info(("ERROR：commit：%s") % (commit))
                title = commit['title']
                title = title.strip()  # 字符串两边去空格
                # logging.info(("INFO：title：%s") % (title))
                # print(("INFO：title：%s") % (title))
                matchStr = re.findall('^B\d+.*|^R\d+.*|^!B\d+.*|^!R\d+.*', title, re.M | re.I | re.S)
                try:
                    matchStr = matchStr[0].split(' ')
                except Exception as e:
                    # logging.info(("INFO：matchStr长度为0：%s") % (e))
                    # print("INFO：matchStr长度为0：%s"%e)
                    pass
                if matchStr:
                    if "msg" in matchStr[0] or "message" in matchStr[0] or "Message" in matchStr[0] or "MESSAGE" in matchStr[0]:
                        sr_list = re.findall('^B\d+|^R\d+|^!B\d+|^!R\d+', matchStr[0], re.M | re.I | re.S)
                        all_sr_list += sr_list
                        # print('1,获取的all_sr_list: ',all_sr_list)
                    else:
                        try:
                            sr_list = matchStr[0].split(',')
                            all_sr_list += sr_list
                            # print('2,获取的all_sr_list: ', all_sr_list)
                        except Exception as e:
                            print(e)

        # 过虑字符串，只取里面的数字
        new_all_sr_list = []
        if all_sr_list:
            all_sr_list = list(set(all_sr_list))  # 除重
            # print('带字母all_sr_list: ',all_sr_list)
            logging.info(("INFO：带字母all_sr_list：%s") % (all_sr_list))
            for string in all_sr_list:
                m = re.findall('\d+', string, re.M | re.I | re.S)
                if m:
                    new_all_sr_list.append(m[0])
        else:
            # print('获取gitlab里的SR号为空！！')
            pass
        return new_all_sr_list

    def get_user_id(self, username):
        # 获取用户ID
        post_url = 'http://gitlab.pab.com.cn/api/v4/users'
        # print('get_user_id  post_url: ', post_url)
        parms_dict = {"username": username}
        try:
            r = requests.get(url=post_url, headers=self.headers, params=parms_dict).text
            r_list = json.loads(r)  # 获取相关信息
            # print(r_list)
            user_id = r_list[0]['id']
        except Exception as e:
            # print('获取 user_id 有误：', e)
            user_id = None
        return user_id

    def add_member_permissions(self, project_type, projectId, user_id, access_level, expires_at):
        '''
        #将成员添加到组或项目

        :param type: 组或项目
        :param user_id: 新成员UM号
        :param access_level:有效的访问级别
        :param expires_at:日期格式为YEAR-MONTH-DAY的日期字符串
        :return:
        '''
        post_url = 'http://gitlab.pab.com.cn/api/v4/%s/%s/members' % (project_type, projectId)
        # print('add_member_permissions  post_url: ',post_url)
        parms_dict = {"user_id": user_id, "access_level": access_level, "expires_at": expires_at, }
        r = requests.post(url=post_url, headers=self.headers, params=parms_dict).text
        r_list = json.loads(r)  # 获取相关信息
        # print('r_list: ', r_list)
        return r_list

    def update_member_permissions(self, project_type, projectId, user_id, access_level, expires_at):
        '''
        #将成员添加到组或项目

        :param type: 组或项目
        :param user_id: 新成员UM号
        :param access_level:有效的访问级别
        :param expires_at:日期格式为YEAR-MONTH-DAY的日期字符串
        :return:
        '''
        post_url = 'http://gitlab.pab.com.cn/api/v4/%s/%s/members/%s' % (project_type, projectId, user_id)
        # print('update_member_permissions  post_url: ',post_url)
        parms_dict = {"access_level": access_level, "expires_at": expires_at, }
        r = requests.put(url=post_url, headers=self.headers, params=parms_dict).text
        r_list = json.loads(r)  # 获取相关信息
        # print('r_list: ', r_list)
        return r_list

    def delete_member_permissions(self, project_type, projectId, user_id):
        '''
        #将成员添加到组或项目

        :param type: 组或项目
        :param user_id: 新成员UM号
        :param access_level:有效的访问级别
        :param expires_at:日期格式为YEAR-MONTH-DAY的日期字符串
        :return:
        '''
        post_url = 'http://gitlab.pab.com.cn/api/v4/%s/%s/members/%s' % (project_type, projectId, user_id)
        # print('delete_member_permissions  post_url: ',post_url)
        r_list = requests.delete(url=post_url, headers=self.headers).text
        # print('r_list: ', r_list)
        return r_list

    def checkout_branch_commit(self,source_branch,target_branch):
        '''
        比较两个分支最后一次提交的信息是否一致
        :param source_branch:  源分支
        :param target_branch:  目标分支
        :return:
        '''

        # 获取分支的最后一次的提交信息
        def get_last_commit(which_branch):
            parms_dict = {"ref_name": which_branch}
            r = requests.get(url=self.url, headers=self.headers, params=parms_dict)
            if r.status_code == 200:
                r_dict = r.json()  # 转为字典
                if r_dict:
                    committed_id=r_dict[0]['id']    # 提交id
                    parent_ids=r_dict[0]['parent_ids']  # 提交父id
                    committed_date=r_dict[0]['committed_date'][:19].replace('T'," ")    # 提交日期
                    committer_name=r_dict[0]['committer_name']  # 提交人
                    result = {"status_code": r.status_code, "data": {"committed_id": committed_id, "parent_ids": parent_ids,
                                                                  "committed_date": committed_date,
                                                                  "committer_name": committer_name}, "message": ""}
                else:   # 找到不此分支则返回空值
                    result = {"status_code": 404, "data": {}, "message": "%s does not exist" % which_branch}
            else:
                r_dict = r.json()  # 转为字典
                result = {"status_code": r.status_code, "data": {}, "message": r_dict["message"]}
            # print(commits)
            return json.dumps(result, sort_keys=True, indent=4)

        release_source=get_last_commit(source_branch)
        release_target=get_last_commit(target_branch)
        # print(release_source)
        # print(release_target)

        release_source = json.loads(release_source) # 字符串转字典
        release_target = json.loads(release_target) # 字符串转字典

        if release_source["status_code"] == 200 and release_target["status_code"] == 200:
            if release_source["data"]["committed_id"] in release_target["data"]["committed_id"]:
                foo = {"status_code": 200, "data": {}, "message": "源分支和目标分支代码完全一致！"}
            elif release_source["data"]["committed_id"] in release_target["data"]["parent_ids"]:
                # foo = {"status_code": 201, "data": {}, "message": "源分支代码已合并到目标分支，源分支和目标分支代码可能不一致！"}
                ########## 如果源分支commit Id存在目标分支父commit Id，且目标分支父commit Id有存在源分支父commit Id中，则代码是一致的，否则不一致！ starting ##########
                release_target["data"]["parent_ids"].remove(release_source["data"]["committed_id"])
                reslut = list(set(release_target["data"]["parent_ids"]).intersection(
                    set(release_source["data"]["parent_ids"])))  # 两个父id列表交集
                if len(reslut) > 0:
                    foo = {"status_code": 200, "data": {}, "message": "源分支代码已合并到目标分支，源分支和目标分支代码一致！"}
                else:
                    foo = {"status_code": 201, "data": {}, "message": "源分支代码已合并到目标分支，源分支和目标分支代码不一致！"}
                ########## 如果源分支commit Id存在目标分支父commit Id，且目标分支父commit Id有存在源分支父commit Id中，则代码是一致的，否则不一致！ end ###############
            elif release_target["data"]["committed_id"] in release_source["data"]["parent_ids"]:
                # foo = {"status_code": 201, "data": {}, "message": "目标分支代码已合并到源分支，源分支和目标分支代码可能不一致！"}
                ########## 如果目标分支commit Id存在源分支父commit Id，且源分支父commit Id有存在目标分支父commit Id中，则代码是一致的，否则不一致！ starting ##########
                release_source["data"]["parent_ids"].remove(release_target["data"]["committed_id"])
                reslut = list(set(release_source["data"]["parent_ids"]).intersection(
                    set(release_target["data"]["parent_ids"])))  # 两个父id列表交集
                if len(reslut) > 0:
                    foo = {"status_code": 200, "data": {}, "message": "源分支代码已合并到目标分支，源分支和目标分支代码一致！"}
                else:
                    foo = {"status_code": 201, "data": {}, "message": "源分支代码已合并到目标分支，源分支和目标分支代码不一致！"}
                ########## 如果目标分支commit Id存在源分支父commit Id，且源分支父commit Id有存在目标分支父commit Id中，则代码是一致的，否则不一致！ end ##############
            else:
                foo = {"status_code": 202, "data": {}, "message": "源分支和目标分支代码不一致！"}
        elif release_source["status_code"] == 404 and release_target["status_code"] == 404:
            foo = {"status_code": 404, "data": {}, "message": "找不到源分支和目标分支！"}
        elif release_source["status_code"] == 404:
            foo = {"status_code": 404, "data": {}, "message": "找不到源分支！"}
        elif release_target["status_code"] == 404:
            foo = {"status_code": 404, "data": {}, "message": "找不到目标分支！"}
        else:
            foo = {"status_code": 404, "data": {}, "message": "获取分支信息有误！"}
        # print(foo)
        return json.dumps(foo, sort_keys=True, indent=4)

    def get_projectInfo_by_id(self):
        # 通过项目id查询项目信息
        url = "http://gitlab.pab.com.cn/api/v4/projects/%s" % (self.project_id)
        r = requests.get(url=url, headers=self.headers)
        # print('状态码：',r.status_code)
        if r.status_code == 200:
            r_dict = r.json()  # 转为字典
            # print(r_dict)
            # print('httl地址: ',r_dict['http_url_to_repo'])
            foo = {"status_code": r.status_code,
                   "data": {"projectId": self.project_id, "http_url": r_dict['http_url_to_repo'],
                            "projectName": r_dict['name']},
                   "message": ""}
        else:
            foo = {"status_code": r.status_code, "data": {"projectId": self.project_id}, "message": r.json()["message"]}
        return json.dumps(foo, sort_keys=True, indent=4)

    def get_projectInfo_by_name(self, projectName):
        # 通过项目名称查询项目信息
        # curl --header "PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/search?scope=projects&search=flight"
        url = "http://gitlab.pab.com.cn/api/v4/search"

        page = 0
        projectInfo_list = []
        foo = {"status_code": 404, "data": {"projectInfo_list": [{"projectName": projectName}]}, "message": "获取信息失败！"}
        while True:
            page += 1
            parms_dict = {"scope": "projects", "search": projectName, "per_page": 100, "page": page}
            r = requests.get(url=url, headers=self.headers, params=parms_dict)
            if r.status_code == 200:
                if len(r.json()) == 0 and page == 1:
                    foo = {"status_code": 201, "data": {"projectInfo_list": [{"projectName": projectName}]},
                           "message": "没有找到对应项目！"}
                    break
                elif len(r.json()) == 0:
                    break
                else:
                    r_list = r.json()
                    for r_dict in r_list:
                        projectInfo_list.append({"projectName": r_dict["name"], "projectId": r_dict["id"],
                                                 "http_url": r_dict["http_url_to_repo"]})

                    foo = {"status_code": r.status_code, "data": {"projectInfo_list": projectInfo_list, },
                           "message": ""}
            else:
                foo = {"status_code": r.status_code, "data": {"projectInfo_list": [{"projectName": projectName}]},
                       "message": r.json()["message"]}
                break
        # print(foo)
        return json.dumps(foo, sort_keys=True, indent=4)

class request(object):
    def __init__(self, url, userToken, serviceName, params):
        '''
        :param url: api url
        :param serviceName: 接口名称
        :param params: 业务参数
        :param userToken: 用户令牌
        '''
        self.url = url
        self.userToken = userToken
        self.serviceName = serviceName
        self.params = params


    def md5(self, valuestr):
        '''
        Encrypt data by using hashlib.md5
        :param valuestr: string, str
        :return: hexdigest
        '''
        md5_str = hashlib.md5()
        md5_str.update(valuestr.encode('utf8'))
        return md5_str.hexdigest()


    def _timestamp(self, date=None):
        '''
        Create timestamp
        :param date: date string, str
        :return: timestamp(millisecond)
        '''
        if not date:
            time_stamp = int(time.mktime(datetime.datetime.now().timetuple()))
        else:
            time_stamp = int(time.mktime(time.strptime(
                date, '%Y-%m-%d %H:%M:%S')) * 1000)
        return time_stamp


    def get_sign(self, clientKey, **args_dict):
        '''
                获取sign值
                :return: sign
            '''
        # key按升序排列
        key_list = sorted(args_dict.keys())
        # print('key按升序排列',key_list)
        param = ''
        for key in key_list:
            item = '%s=%s&' % (key, args_dict[key])
            param += item
        param += clientKey
        # print('# 参加签名url: ',param)
        param_url = urllib.parse.quote_plus(param.encode('utf8'))
        sign = self.md5(param_url).upper()
        return sign


    def merger_to_dicts(self, dict_x, dict_y):
        dict_sum = dict_x.copy()
        dict_sum.update(dict_y)
        return dict_sum


    def run(self):
        '''
        请求接口
        :param url: 接口url
        :param serviceName: 接口名
        :param params: 接口data，params部分数据，字典格式
        :return: respone响应内容
        '''
        headers = {'Content-Type': 'application/json'}

        clientKey = '0e0e7a0e97164e79ba29824be0e77d67'
        clientCode = 'BRON-COSS'
        timestamp = str(self._timestamp())
        # serviceVersion = '1.0.0'
        header = {
            'clientCode': clientCode,
            'serviceName': self.serviceName,
            'userToken': self.userToken,
            # 'serviceVersion': serviceVersion,
            'timestamp': timestamp
        }
        dicts = self.merger_to_dicts(header, self.params)  # 参与签名参数
        sign = self.get_sign(clientKey, **dicts)  # 获取sign值
        header['sign'] = sign  # 请求header信息
        params_dict = {'header': header, 'params': self.params}  # 请求data
        # print(params_dict)
        respone = requests.post(url=self.url, headers=headers, data=json.dumps(params_dict))  # 请求api
        return respone


class get_releaseName_info(object):
    '''获取空间版本信息'''

    def __init__(self, domain_name):
        self.url = 'http://wb-pab.paic.com.cn/api/service'
        self.serviceName = 'alm.project.release'
        self.params = {'projectAbbrName': domain_name}
        self.userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'


    def request(self):
        respone = request(self.url, self.userToken, self.serviceName, self.params).run()
        # print('响应内容字符串形式(精准): ',respone.apparent_encoding)
        # print('响应内容字符串形式: ',respone.encoding)
        return respone


    def get_releaseName(self, respone):
        '''
        :param respone: 响应内容
        :return: release_name_list  未投产版本列表
        '''
        releaseName_dict = {}
        planReleaseEndDate_dict = {}  # 存放版本的投产日期
        try:
            result = respone.json()
            for releaseInfo in result['data']:
                if releaseInfo['releaseState'] == 'Todo':  # 过虑已发布的版本
                    # print("版本号：",releaseInfo['releaseName'])
                    # print("版本创建时间：",releaseInfo['createdDate'])
                    # 存放版本和版本的创建时间值，如：[{"BCON-COSS4.46.0":"2020-10-17 15:24:21"}]
                    releaseName_dict[releaseInfo['releaseName']] = releaseInfo['createdDate']
                    planReleaseEndDate_dict[releaseInfo['releaseName']] = releaseInfo['planReleaseEndDate']
        except:
            print('非json数据, 解析失败, text数据如下：', respone.text)
        return releaseName_dict, planReleaseEndDate_dict


def split_line(mark, number):
    '''分割线'''
    print(mark * number)


# 查询指定子系统或空间下卡片（用户故事、缺陷、任务-有子卡片拆在用户故事里的任务卡片）
def get_all_card(domain, planName, stateDetail):
    '''
    :param domain: 神兵空间简称
    :param planName:  版本号，如：BRON-COSS4.46.0
    :param stateDetail:  卡片状态
    :return:
    '''
    # print('domain: ',domain)
    # print('planName: ',planName)
    # print('stateDetail: ',stateDetail)

    print('正在获取卡片ID...')
    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.subsys.cards'
    # beginTime=123456789456  # 开始时间毫秒数（创建时间）
    # 获取用户故事卡片
    # story_params = {'projectAbbrName': domain,'issueType':'Story','beginTime':beginTime}
    story_params = {'projectAbbrName': domain, 'issueType': 'Story'}
    story_cards = request(url, userToken, serviceName, story_params).run()
    # 获取缺陷卡片
    # defect_params = {'projectAbbrName': domain, 'issueType': 'Defect','beginTime':beginTime}
    defect_params = {'projectAbbrName': domain, 'issueType': 'Defect'}
    defect_cards = request(url, userToken, serviceName, defect_params).run()

    # 获取任务卡片
    # assignment_params = {'projectAbbrName': domain, 'issueType': 'Defect','beginTime':beginTime}
    assignment_params = {'projectAbbrName': domain, 'issueType': 'Assignment'}
    assignment_cards = request(url, userToken, serviceName, assignment_params).run()

    # 获取指定版本下状态为"开发完成待部署"的用户故事和缺陷卡片SR号，如：BRON-COSS#1327
    cards_list = []  # 存放用户故事和缺陷卡片
    uncode_cards_list = []  # 存放用户故事和缺陷卡片，实现方式为非编码的卡片
    story_cards_sr_list = []  # 存放用户故事卡片号
    _all_story_cards_sr_list = []  # 存放用户故事卡片号，不分状态，用于任务卡片
    defect_cards_sr_list = []  # 存放缺陷卡片号
    assignment_cards_sr_list = []  # 存放任务卡片号
    all_cards_stateDetail_list = []  # 存放所有卡片的当前stateDetail状态

    story_cards_list = story_cards.json()['data']  # 获取用户故事类卡片的对象
    for attr_dict in story_cards_list:
        if attr_dict['planName'] == planName:
            _all_story_cards_sr_list.append(attr_dict['wizardGlobalId'])
            # print('所有用户故事卡片号，不分状态_all_story_cards_sr_listt：', _all_story_cards_sr_list)
            all_cards_stateDetail_list.append("%s: %s" % (attr_dict['wizardGlobalId'], attr_dict['stateDetail']))
            if attr_dict['stateDetail'] == stateDetail:
                story_cards_sr_list.append(attr_dict['wizardGlobalId'])
                if attr_dict['customFields']:  # 如果有自定以的字段,即卡片没有非编码和编码之分
                    for customFields in ast.literal_eval(attr_dict['customFields']):  # 字符串转列表同时再转成字典
                        # 获取实现方式为非编码状态的卡片
                        if customFields['name'] == '实现方式' and customFields['value'] == '非编码':
                            uncode_cards_list.append(attr_dict['wizardGlobalId'])
                            break
                    else:
                        cards_list.append(attr_dict['wizardGlobalId'])
                else:
                    cards_list.append(attr_dict['wizardGlobalId'])

    defect_cards_list = defect_cards.json()['data']  # 获取缺陷类卡片的对象
    for attr_dict in defect_cards_list:
        if attr_dict['planName'] == planName:
            all_cards_stateDetail_list.append("%s: %s" % (attr_dict['wizardGlobalId'], attr_dict['stateDetail']))
            if attr_dict['stateDetail'] == stateDetail:
                defect_cards_sr_list.append(attr_dict['wizardGlobalId'])
                if attr_dict['customFields']:  # 如果有自定以的字段,即卡片没有非编码和编码之分
                    for customFields in ast.literal_eval(attr_dict['customFields']):  # 字符串转列表再转成字典
                        # 获取实现方式为非编码状态的卡片
                        if customFields['name'] == '实现方式' and customFields['value'] == '非编码':
                            uncode_cards_list.append(attr_dict['wizardGlobalId'])
                        break
                    else:
                        cards_list.append(attr_dict['wizardGlobalId'])
                else:
                    cards_list.append(attr_dict['wizardGlobalId'])

    assignment_cards_list = assignment_cards.json()['data']  # 获取任务类卡片的对象
    for attr_dict in assignment_cards_list:
        # print('任务卡片信息：',attr_dict)
        if attr_dict['parentGlobalId'] in _all_story_cards_sr_list:  # 如果任务卡片属于该版本内的用户故事
            all_cards_stateDetail_list.append("%s: %s" % (attr_dict['wizardGlobalId'], attr_dict['stateDetail']))
            if attr_dict['stateDetail'] == stateDetail:
                assignment_cards_sr_list.append(attr_dict['wizardGlobalId'])
                if attr_dict['customFields']:  # 如果有自定以的字段,即卡片没有非编码和编码之分
                    for customFields in ast.literal_eval(attr_dict['customFields']):  # 字符串转列表再转成字典
                        # 获取实现方式为非编码状态的卡片
                        if customFields['name'] == '实现方式' and customFields['value'] == '非编码':
                            uncode_cards_list.append(attr_dict['wizardGlobalId'])
                        break
                    else:
                        cards_list.append(attr_dict['wizardGlobalId'])
                else:
                    cards_list.append(attr_dict['wizardGlobalId'])

    # 过虑字符串，只取里面的数字
    new_cards_list = []
    # print('所有卡片cards_list：',cards_list)
    # print('所有卡片all_cards_stateDetail_list：',all_cards_stateDetail_list)
    for str in cards_list:
        # m = re.findall('\d+', str,re.M|re.I|re.S)
        # new_cards_list.append(m[0])
        number = str.split('#')[-1]
        new_cards_list.append(number)

    # 过虑字符串，只取里面的数字
    new_uncode_cards_list = []
    for str in uncode_cards_list:
        # m = re.findall('\d+', str, re.M | re.I | re.S)
        # new_uncode_cards_list.append(m[0])
        number = str.split('#')[-1]
        new_uncode_cards_list.append(number)

    return new_cards_list, new_uncode_cards_list, story_cards_sr_list, defect_cards_sr_list, assignment_cards_sr_list, all_cards_stateDetail_list


def get_defect_and_story_cards(domain, planName):
    print('###### 获取神兵空间下用户故事和缺陷类卡片 starting ######')
    # print('domain: ', domain)
    # print('planName: ', planName)

    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.subsys.cards'

    # 获取用户故事卡片
    story_params = {'projectAbbrName': domain, 'issueType': 'Story'}
    story_cards = request(url, userToken, serviceName, story_params).run()
    # 获取缺陷卡片
    defect_params = {'projectAbbrName': domain, 'issueType': 'Defect'}
    defect_cards = request(url, userToken, serviceName, defect_params).run()

    # print('获取用户故事卡片: ',story_cards.json())
    # print('获取缺陷卡片: ',defect_cards.json())

    all_cards_stateDetail_dict = {}  # 存放所有卡片的当前stateDetail状态

    story_cards_list = story_cards.json()['data']  # 获取用户故事类卡片的对象
    for attr_dict in story_cards_list:
        if attr_dict['planName'] == planName:
            all_cards_stateDetail_dict[attr_dict['wizardGlobalId']] = attr_dict['stateDetail']

    defect_cards_list = defect_cards.json()['data']  # 获取缺陷类卡片的对象
    for attr_dict in defect_cards_list:
        if attr_dict['planName'] == planName:
            all_cards_stateDetail_dict[attr_dict['wizardGlobalId']] = attr_dict['stateDetail']

    print(all_cards_stateDetail_dict)
    print('###### 获取神兵空间下用户故事和缺陷类卡片 end ---- ######')

    return all_cards_stateDetail_dict


def update_card_state(wizardGlobalId):
    '''
    修改卡片状态

    :params: wizardGlobalId: 业务全局ID, 示例：BRON-COSS#1280
             stateDetail: 状态名称, 示例：测试完成
    :return: respone
    '''
    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.need.modify.byGlobalId'
    params = {
        'wizardGlobalId': wizardGlobalId,
        'stateDetail': '已部署待自测'
    }
    respone = request(url, userToken, serviceName, params).run()
    print(respone.json())  # 字典
    # 失败：{'data': {}, 'header': {'ret': 100, 'errorMsg': 'error :您无权操作'}}
    # 成功：{'data': 'TEST12#1', 'header': {'ret': 0}}
    card_dict = respone.json()
    header = card_dict["header"]

    ret = header['ret']
    if ret == 0:
        print("%s卡片移动成功！" % wizardGlobalId)
        return ['True']
    else:
        if "卡片变为已部署待自测状态前需要填写" in header["errorMsg"]:
            print("%s卡片移动成功！" % wizardGlobalId)
            return ['True']
        else:
            print("%s卡版移动失败！ " % wizardGlobalId, header["errorMsg"])
            return ['False', header["errorMsg"]]


def modify_card_state(wizardGlobalId, stateDetail):
    '''
    修改卡片状态

    :params: wizardGlobalId: 业务全局ID, 示例：BRON-COSS#1280
             stateDetail: 状态名称, 示例：测试完成
    :return: respone
    '''
    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.need.modify.byGlobalId'
    params = {
        'wizardGlobalId': wizardGlobalId,
        'stateDetail': stateDetail
    }
    respone = request(url, userToken, serviceName, params).run()
    print(respone.json())  # 字典
    # 失败：{'data': {}, 'header': {'ret': 100, 'errorMsg': 'error :您无权操作'}}
    # 成功：{'data': 'TEST12#1', 'header': {'ret': 0}}
    card_dict = respone.json()
    header = card_dict["header"]

    ret = header['ret']
    if ret == 0:
        print("%s卡片移动成功！" % wizardGlobalId)
        return ['True']
    else:
        if "卡片变为%s状态前需要填写" % stateDetail in header["errorMsg"]:
            print("%s卡片移动成功！" % wizardGlobalId)
            return ['True']
        else:
            print("%s卡版移动失败！ " % wizardGlobalId, header["errorMsg"])
            return ['False', header["errorMsg"]]


# 获取空间的卡片所有泳道名称
def get_cards_status_name(domain):
    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.project.issueState'
    params = {'projectAbbrName': domain}
    respone = request(url, userToken, serviceName, params).run()
    # print(respone.json())

    card_status_name_list = []
    try:
        # print(respone.json()['data']['Story'])
        for name in respone.json()['data']['Story']:  # 获取卡片所有泳道名称
            card_status_name_list.append(name['name'])
    except Exception as e:
        print('获取卡片所有泳道名称报错：', e)
        print(respone.json())
    return card_status_name_list


def timedTask_move_crads(userName, domain_name, zoneName, projectId, planName, start_time):
    # 从神兵接口获取当前版本状态名为"开发完成待部署"的所有卡片
    stateDetail = '开发完成待部署'
    projectId = projectId.split(',')  # 转成列表

    cards_list, uncode_cards_list, story_cards_sr_list, defect_cards_sr_list, assignment_cards_sr_list, all_cards_stateDetail_list = get_all_card(
        zoneName, planName, stateDetail)

    print(planName, '当前分支卡片如下：', cards_list)
    print(planName, '当前分支非编码卡片如下: ', uncode_cards_list)
    print("=" * 100)
    print('在神兵（开发完成待部署状态） 用户故事 卡片：', story_cards_sr_list)
    print('在神兵（开发完成待部署状态） 缺陷 卡片：', defect_cards_sr_list)
    print('在神兵（开发完成待部署状态） 任务 卡片：', assignment_cards_sr_list)
    print("=" * 100)


    if cards_list + uncode_cards_list:  # 如果神兵没有卡片，则不移动卡片
        '''从gitlab接口，commits信息中获取SR号  start'''
        # 处理时间格式
        # start_time = start_time.replace("T", " ")
        # start_time = start_time + ":00"
        print('start_time: ', start_time)

        which_branch = 'Release_' + planName
        print('gitlab分支名：', which_branch)
        # 获取该用户下的所有领域名
        domain_file = 'config/domain_config/%s_domain_config.ini' % userName
        read_domain = getConfig(domain_file)
        private_token = read_domain.get_value(domain_name, 'privatekey')
        server_name = '/repository/commits'

        '''多线程 starting'''
        def get_gitlab_sr(SR_list, gitlab_progectId, server_name, private_token, which_branch, start_time):
            branch_info = request_gitlab_api(gitlab_progectId, server_name, private_token)
            SR_list += branch_info.deploy_go_by_time(which_branch, start_time)

        SR_list = []  # 储存所有projectId上的commits中的SR号
        thread_list = []
        for id in projectId:
            t = Thread(target=get_gitlab_sr,
                       args=(SR_list, id, server_name, private_token, which_branch, start_time))  # 创建线程
            t.start()  # 执行线程
            thread_list.append(t)  # 保存线程对象

        # 等待所有线程结束
        for thread in thread_list:
            thread.join()

        # 单进程方式 start...
        # SR_list=[]  # 储存所有projectId上的commits中的SR号
        # for id in projectId:
        #     branch_info = request_gitlab_api(id, server_name, private_token)
        #     SR_list+=branch_info.deploy_go_by_time(which_branch, start_time)
        # 单进程方式 end...

        print('储存所有projectId上的commits中的SR号(未除重): ', SR_list)

        # 去重，因为提交代码到不同的库时会使用相同的SR号，所以要去重
        SR_list = list(set(SR_list))
        print('【定时移动】在gitlab找到的所有SR号(已除重): ', SR_list)

        '''多线程 end'''

        move_cards = []  # 储存已经被移动的卡片
        unmove_cards = []  # 储存没有被移动的卡片
        for sr in cards_list:
            # 有提交记录或非编码的则移动该卡片
            if sr in SR_list:
                wizardGlobalId = zoneName + "#" + sr
                print('%s此卡片在gitlab上有commits信息' % wizardGlobalId)

                status_code = update_card_state(wizardGlobalId)  # 执行卡片移动
                if len(status_code) == 1:
                    if wizardGlobalId in story_cards_sr_list:
                        move_cards.append("【用户故事】%s" % wizardGlobalId)
                    elif wizardGlobalId in defect_cards_sr_list:
                        move_cards.append("【缺陷】%s" % wizardGlobalId)
                    elif wizardGlobalId in assignment_cards_sr_list:
                        move_cards.append("【任务】%s" % wizardGlobalId)
                    else:
                        move_cards.append("【其他】%s" % wizardGlobalId)
                else:
                    if wizardGlobalId in story_cards_sr_list:
                        unmove_cards.append("【用户故事】%s: %s" % (wizardGlobalId, status_code[1]))
                    elif wizardGlobalId in defect_cards_sr_list:
                        unmove_cards.append("【缺陷】%s: %s" % (wizardGlobalId, status_code[1]))
                    elif wizardGlobalId in assignment_cards_sr_list:
                        unmove_cards.append("【任务】%s: %s" % (wizardGlobalId, status_code[1]))
                    else:
                        unmove_cards.append("【其他】%s: %s" % (wizardGlobalId, status_code[1]))
                    print("%s: " % wizardGlobalId, status_code[1])
            else:
                wizardGlobalId = zoneName + "#" + sr
                if wizardGlobalId in story_cards_sr_list:
                    unmove_cards.append("【用户故事】%s: 没有提交代码记录！" % wizardGlobalId)
                elif wizardGlobalId in defect_cards_sr_list:
                    unmove_cards.append("【缺陷】%s: 没有提交代码记录！" % wizardGlobalId)
                else:
                    unmove_cards.append("【其他】%s: 没有提交代码记录！" % wizardGlobalId)
                # print('%s此卡片不曾在gitlab上有commits信息' % wizardGlobalId)
                # print("%s: 没有提交代码记录！" % wizardGlobalId)

        move_uncode_cards = []
        for sr in uncode_cards_list:
            wizardGlobalId = zoneName + "#" + sr
            print('%s此卡片为非编码卡版，直接移动！' % wizardGlobalId)
            status_code = update_card_state(wizardGlobalId)
            if len(status_code) == 1:
                if wizardGlobalId in story_cards_sr_list:
                    move_cards.append("【用户故事】%s" % wizardGlobalId)
                elif wizardGlobalId in defect_cards_sr_list:
                    move_cards.append("【缺陷】%s" % wizardGlobalId)
                else:
                    move_cards.append("【其他】%s" % wizardGlobalId)
            else:
                if wizardGlobalId in story_cards_sr_list:
                    unmove_cards.append("【用户故事】%s: %s" % (wizardGlobalId, status_code[1]))
                elif wizardGlobalId in defect_cards_sr_list:
                    unmove_cards.append("【缺陷】%s: %s" % (wizardGlobalId, status_code[1]))
                else:
                    unmove_cards.append("【其他】%s: %s" % (wizardGlobalId, status_code[1]))
                print("%s: " % wizardGlobalId, status_code[1])

        print("INFO：" + "-" * 50 + " 定时任务执行结果 starting " + "-" * 50)
        print("INFO：执行用户：%s" % userName)
        print("INFO：执行领域：%s" % domain_name)
        print("INFO：执行分支：%s" % planName)
        print("INFO：执行时间：%s" % datetime.datetime.now())
        print("INFO：执行结果" + " 已被移动的卡片： %s" % move_cards)
        print("INFO：执行结果" + " 未被移动的卡片： %s" % unmove_cards)
        print("INFO：" + "-" * 50 + " 定时任务执行结果 end " + "-" * 50)
        try:
            logging.info("INFO：" + "-" * 50 + " 定时任务执行结果 starting " + "-" * 50)
            logging.info("INFO：执行用户：%s" % userName)
            logging.info("INFO：执行领域：%s" % domain_name)
            logging.info("INFO：执行分支：%s" % planName)
            logging.info("INFO：执行时间：%s" % datetime.datetime.now())
            logging.info("INFO：执行结果" + " 已被移动的卡片： %s" % move_cards)
            logging.info("INFO：执行结果" + " 未被移动的卡片： %s" % unmove_cards)
            logging.info("INFO：" + "-" * 50 + " 定时任务执行结果 end " + "-" * 50)
        except Exception as e:
            print(e)
    else:
        move_cards_str = '%s神兵空间没有"开发完成待部署"状态的卡片，不需要移动卡片！' % zoneName
        print("INFO：" + "-" * 50 + " 定时任务执行结果 starting " + "-" * 50)
        print("INFO：执行用户：%s" % userName)
        print("INFO：执行领域：%s" % domain_name)
        print("INFO：执行分支：%s" % planName)
        print("INFO：执行时间：%s" % datetime.datetime.now())
        print("INFO：执行结果：" + move_cards_str)
        print("INFO：" + "-" * 50 + " 定时任务执行结果 end " + "-" * 50)
        try:
            logging.info("INFO：" + "-" * 50 + " 定时任务执行结果 starting " + "-" * 50)
            logging.info("INFO：执行用户：%s" % userName)
            logging.info("INFO：执行领域：%s" % domain_name)
            logging.info("INFO：执行分支：%s" % planName)
            logging.info("INFO：执行时间：%s" % datetime.datetime.now())
            logging.info("INFO：执行结果：" + move_cards_str)
            logging.info("INFO：" + "-" * 50 + " 定时任务执行结果 end " + "-" * 50)
        except Exception as e:
            print(e)

        '''从gitlab接口，commits信息中获取SR号  end'''


def modifyCardStatus(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(modifyCardStatus.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【神兵卡片管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您尚未登录超级用户，请先登录！！"
        return render(request, 'software/index.html', locals())

    # 获取GET请求时领域名
    if request.GET.get('domain_name'):
        domain_name = request.GET.get('domain_name')
    # 获取POST请求时领域名
    elif request.POST.get('domain_name'):
        domain_name = request.POST.get('domain_name')
    else:
        domain_name = None

    # 获取GET请求时停留在哪个功能页面
    if request.GET.get('feature'):
        myMenu = request.GET.get('feature')
        # print('myMenu: ',myMenu)
    # 获取POST请求时停留在哪个功能页面
    elif request.POST.get('feature'):
        myMenu = request.POST.get('feature')
        # print('当前菜单位置: ', myMenu)
    else:
        myMenu = 'myMenu0'

    if request.method == 'POST':

        ####### 更改领域 starting #######
        if request.POST.get('zone_name'):
            modify_zone_name = request.POST.get('zone_name')
            modify_domain_name_management = request.POST.get('domain_name_management')  # 领域名
            modify_projectId = request.POST.get('projectId')  # 项目ID
            modify_privateKey = request.POST.get('privateKey')  # privateKey
            # 去空格
            modify_zone_name = modify_zone_name.replace(" ", "")
            modify_domain_name_management = modify_domain_name_management.replace(" ", "")
            modify_projectId = modify_projectId.replace(" ", "")
            modify_privateKey = modify_privateKey.replace(" ", "")
            # 中文逗号转英文逗号
            modify_projectId = modify_projectId.replace("，", ",")
            for id_str in modify_projectId:
                if id_str not in "0123456789,":
                    new_domain_msg = "项目ID 输入格式有误！"
                    return render(request, 'software/modifyCardStatus.html', locals())
            if modify_projectId[0] == "," or modify_projectId[-1] == ",":
                new_domain_msg = "输入有误, 必须以数字开头和结尾！"
                return render(request, 'software/modifyCardStatus.html', locals())

            # 修改节点
            domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
            modfiy_domain = getConfig(domain_file)
            if modfiy_domain.check_section(modify_zone_name):
                modfiy_domain.add_section(modify_zone_name)
                modfiy_domain.set_section(modify_zone_name, 'domain_name_management', modify_domain_name_management)
                modfiy_domain.set_section(modify_zone_name, 'projectId', modify_projectId)
                modfiy_domain.set_section(modify_zone_name, 'privateKey', modify_privateKey)
                modfiy_domain.save()
                new_domain_msg = '更改成功!'
            else:
                new_domain_msg = '更改失败，领域不存在!'
        ####### 更改领域 end ---- #######

        ####### 新增领域 starting #######
        if request.POST.get('new_zone_name'):
            # 获取用户输入值
            new_zone_name = request.POST.get('new_zone_name')  # 空间别名
            new_domain_name_management = request.POST.get('new_domain_name_management')  # 领域名
            new_projectId = request.POST.get('new_projectId')  # 项目ID
            new_privateKey = request.POST.get('new_privateKey')  # privateKey
            # 去空格
            new_zone_name = new_zone_name.replace(" ", "")
            new_domain_name_management = new_domain_name_management.replace(" ", "")
            new_projectId = new_projectId.replace(" ", "")
            new_privateKey = new_privateKey.replace(" ", "")
            # 中文逗号转英文逗号
            new_projectId = new_projectId.replace("，", ",")
            for id_str in new_projectId:
                if id_str not in "0123456789,":
                    new_domain_msg = "项目ID 输入格式有误！"
                    return render(request, 'software/modifyCardStatus.html', locals())
            if new_projectId[0] == "," or new_projectId[-1] == ",":
                new_domain_msg = "输入有误, 必须以数字开头和结尾！"
                return render(request, 'software/modifyCardStatus.html', locals())

            domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
            if os.path.exists(domain_file):
                # print('文件已存在!')
                pass
            else:
                with open(domain_file, 'a+') as f:
                    # print('文件不存在!')
                    pass

            # 添加节点
            new_domain = getConfig(domain_file)
            if new_domain.check_section(new_zone_name):
                new_domain_msg = '新增失败，领域已存在!'
            else:
                new_domain.add_section(new_zone_name)
                new_domain.set_section(new_zone_name, 'domain_name_management', new_domain_name_management)
                new_domain.set_section(new_zone_name, 'projectId', new_projectId)
                new_domain.set_section(new_zone_name, 'privateKey', new_privateKey)
                new_domain.save()
                new_domain_msg = '新增领域成功!'
        ####### 新增领域 end ---- #######

        ####### 删除领域 starting #######
        if request.POST.get('del_domain_name'):
            del_domain_name = request.POST.get('del_domain_name')
            # print('del_domain_name: ', del_domain_name)
            domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
            del_domain = getConfig(domain_file)
            del_domain.remove_section(del_domain_name)
            del_domain.save()
            new_domain_msg = '%s 删除成功！!' % del_domain_name
        ####### 删除领域 end ---- #######

        ####### 按时间移动卡片 starting #######
        if myMenu == 'myMenu0':
            if request.POST.get('move_card_by_time'):
                # 获取用户输入的值，用于调用神兵和gitlab接口
                domain_name = request.POST.get('domain_name')  # 获取领域别名
                # print('领域别名domain_name: ', domain_name)
                domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
                domain = getConfig(domain_file)
                domain_name_management = domain.get_value(domain_name, 'domain_name_management')  # 获取神兵空间名，英文简称
                planName = request.POST.get('branch')
                # print('planName: ', planName)
                projectId = request.POST.getlist('projectId')
                start_time = request.POST.get('start_time')
                # print('projectId: ', projectId)
                # print('start_time: ', start_time)

                # 从神兵接口获取当前版本状态名为"开发完成待部署"的所有卡片
                stateDetail = '开发完成待部署'
                cards_list, uncode_cards_list, story_cards_sr_list, defect_cards_sr_list, assignment_cards_sr_list, all_cards_stateDetail_list = get_all_card(
                    domain_name_management, planName, stateDetail)

                print(planName, '当前分支卡片如下：', cards_list)
                print(planName, '当前分支非编码卡片如下: ', uncode_cards_list)
                print("=" * 100)
                print('在神兵（开发完成待部署状态） 用户故事 卡片：', story_cards_sr_list)
                print('在神兵（开发完成待部署状态） 缺陷 卡片：', defect_cards_sr_list)
                print('在神兵（开发完成待部署状态） 任务 卡片：', assignment_cards_sr_list)
                print('在神兵（开发完成待部署状态） 所有 卡片：', all_cards_stateDetail_list)
                print("=" * 100)

                if cards_list + uncode_cards_list:  # 如果神兵没有卡片，则不移动卡片
                    '''从gitlab接口，commits信息中获取SR号  start'''
                    # 处理时间格式
                    start_time = start_time.replace("T", " ")
                    start_time = start_time + ":00"
                    # print('start_time: ', start_time)

                    which_branch = 'Release_' + planName
                    # print('gitlab分支名：',which_branch)
                    # 获取该用户下的所有领域名
                    domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
                    read_domain = getConfig(domain_file)
                    private_token = read_domain.get_value(domain_name, 'privatekey')
                    server_name = '/repository/commits'

                    '''多线程 starting'''
                    def get_gitlab_sr(SR_list, gitlab_progectId, server_name, private_token, which_branch, start_time):
                        branch_info = request_gitlab_api(gitlab_progectId, server_name, private_token)
                        SR_list += branch_info.deploy_go_by_time(which_branch, start_time)

                    SR_list = []  # 储存所有projectId上的commits中的SR号
                    thread_list = []
                    for id in projectId:
                        t = Thread(target=get_gitlab_sr, args=(SR_list, id, server_name, private_token, which_branch, start_time))  # 创建线程
                        t.start()  # 执行线程
                        thread_list.append(t)  # 保存线程对象

                    # 等待所有线程结束
                    for thread in thread_list:
                        thread.join()

                    # 单进程方式 start...
                    # SR_list=[]  # 储存所有projectId上的commits中的SR号
                    # for id in projectId:
                    #     branch_info = request_gitlab_api(id, server_name, private_token)
                    #     SR_list+=branch_info.deploy_go_by_time(which_branch, start_time)
                    # 单进程方式 end...

                    # print('储存所有projectId上的commits中的SR号(未除重): ', SR_list)

                    # 去重，因为提交代码到不同的库时会使用相同的SR号，所以要去重
                    SR_list = list(set(SR_list))
                    print('【按时间移动】在gitlab找到的所有SR号(已除重): ', SR_list)

                    '''多线程 end'''


                    move_cards = []
                    unmove_cards = []
                    for sr in cards_list:
                        # 有提交记录或非编码的则移动该卡片
                        if sr in SR_list:
                            wizardGlobalId = domain_name_management + "#" + sr
                            # print('%s此卡片在gitlab上有commits信息' % wizardGlobalId)

                            status_code = update_card_state(wizardGlobalId)  # 执行卡片移动
                            if len(status_code) == 1:
                                if wizardGlobalId in story_cards_sr_list:
                                    move_cards.append("【用户故事】%s" % wizardGlobalId)
                                elif wizardGlobalId in defect_cards_sr_list:
                                    move_cards.append("【缺陷】%s" % wizardGlobalId)
                                elif wizardGlobalId in assignment_cards_sr_list:
                                    move_cards.append("【任务】%s" % wizardGlobalId)
                                else:
                                    move_cards.append("【其他】%s" % wizardGlobalId)
                            else:
                                if wizardGlobalId in story_cards_sr_list:
                                    unmove_cards.append("【用户故事】%s: %s" % (wizardGlobalId, status_code[1]))
                                elif wizardGlobalId in defect_cards_sr_list:
                                    unmove_cards.append("【缺陷】%s: %s" % (wizardGlobalId, status_code[1]))
                                elif wizardGlobalId in assignment_cards_sr_list:
                                    unmove_cards.append("【任务】%s: %s" % (wizardGlobalId, status_code[1]))
                                else:
                                    unmove_cards.append("【其他】%s: %s" % (wizardGlobalId, status_code[1]))
                                print("%s: " % wizardGlobalId, status_code[1])
                        else:
                            wizardGlobalId = domain_name_management + "#" + sr
                            if wizardGlobalId in story_cards_sr_list:
                                unmove_cards.append("【用户故事】%s: 没有提交代码记录！" % wizardGlobalId)
                            elif wizardGlobalId in defect_cards_sr_list:
                                unmove_cards.append("【缺陷】%s: 没有提交代码记录！" % wizardGlobalId)
                            else:
                                unmove_cards.append("【其他】%s: 没有提交代码记录！" % wizardGlobalId)
                                # print('%s此卡片不曾在gitlab上有commits信息' % wizardGlobalId)
                                # print("%s: 没有提交代码记录！" % wizardGlobalId)

                    move_uncode_cards = []
                    for sr in uncode_cards_list:
                        wizardGlobalId = domain_name_management + "#" + sr
                        print('%s此卡片为非编码卡版，直接移动！' % wizardGlobalId)
                        status_code = update_card_state(wizardGlobalId)
                        if len(status_code) == 1:
                            if wizardGlobalId in story_cards_sr_list:
                                move_cards.append("【用户故事】%s" % wizardGlobalId)
                            elif wizardGlobalId in defect_cards_sr_list:
                                move_cards.append("【缺陷】%s" % wizardGlobalId)
                            else:
                                move_cards.append("【其他】%s" % wizardGlobalId)
                        else:
                            if wizardGlobalId in story_cards_sr_list:
                                unmove_cards.append("【用户故事】%s: %s" % (wizardGlobalId, status_code[1]))
                            elif wizardGlobalId in defect_cards_sr_list:
                                unmove_cards.append("【缺陷】%s: %s" % (wizardGlobalId, status_code[1]))
                            else:
                                unmove_cards.append("【其他】%s: %s" % (wizardGlobalId, status_code[1]))
                            print("%s: " % wizardGlobalId, status_code[1])
                else:
                    move_cards_str = '%s神兵空间没有"开发完成待部署"状态的卡片，不需要移动卡片！' % domain_name_management
                    print(move_cards_str)
                    '''从gitlab接口，commits信息中获取SR号  end'''
        ####### 按时间移动卡片 end ---- #######

        ####### 定时任务 starting #######
        if myMenu == 'myMenu1':
            # 创建定时任务
            if request.POST.get('createTimedTask'):
                loginUser = request.session['user_name']  # 当前登录用户
                domain_name = request.POST.get('domain_name')  # 获取领域名
                zoneName = request.POST.get('zoneName')  # 获取当前领域神兵空间英文简称
                # print('# 获取当前领域神兵空间英文简称: ',zoneName)
                branch = request.POST.get('branch')  # 获取分支
                projectId_list = request.POST.getlist('projectId')  # 获取代码库ID
                start_time_str = request.POST.get('start_time')  # 获取任务开始时间
                end_time_str = request.POST.get('end_time')  # 获取任务结束时间
                time_intervals = request.POST.get('time_intervals')  # 获取重复执行任务时间间隔
                time_type = request.POST.get('time_type')  # 获取时间单位

                # 字符串转成时间类型
                start_time_str = start_time_str.replace("T", " ") + ":00"
                end_time_str = end_time_str.replace("T", " ") + ":00"
                start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

                # 列表转字符串
                projectId = ','.join(projectId_list)

                # 将定时任务信息储存到数据库
                addTask = TimedTaskForMoveCard.timedTask.create()
                addTask.userName = request.session['user_name']
                addTask.domainName = domain_name
                addTask.zoneName = zoneName
                addTask.branch = branch
                addTask.projectId = projectId
                addTask.startTime = start_time
                addTask.endTime = end_time
                addTask.intervalTime = time_intervals
                addTask.timeType = time_type
                addTask.save()

                ''' 创建任务 starting '''
                # 如果用户名不为空，则只获取该用户下的定时任务数据，降序排列
                getTimedTaskInfo_list = TimedTaskForMoveCard.timedTask.filter(userName=loginUser, domainName=domain_name,
                                                                              branch=branch, projectId=projectId,
                                                                              startTime=start_time, endTime=end_time,
                                                                              intervalTime=time_intervals,
                                                                              timeType=time_type).order_by('-id')

                # 取的第一个值即是最近要创建的定时任务,实际情况应该只有一条数据，极少有多条数据
                id = str(getTimedTaskInfo_list[0].id)
                user_name = getTimedTaskInfo_list[0].userName
                domain_name = getTimedTaskInfo_list[0].domainName
                zone_name = getTimedTaskInfo_list[0].zoneName
                # print('获取数据库中的空间简称：',zone_name)
                branch = getTimedTaskInfo_list[0].branch
                project_id = getTimedTaskInfo_list[0].projectId
                start_time = getTimedTaskInfo_list[0].startTime.strftime("%Y-%m-%d %H:%M:%S")
                end_time = getTimedTaskInfo_list[0].endTime.strftime("%Y-%m-%d %H:%M:%S")
                interval_time = int(getTimedTaskInfo_list[0].intervalTime)
                time_type = getTimedTaskInfo_list[0].timeType

                # 获取该用户下的所有领域名
                domain_file_path = 'config/domain_config/%s_branch_config.ini' % user_name
                getDomainInfo = getConfig(domain_file_path)
                try:
                    create_branch_time = getDomainInfo.get_value(domain_name, branch)  # 获取当前版本创建时间
                    # print('获取神兵空间简称: ', create_branch_time)
                except Exception as e:
                    print(e)
                    print('版本创建时间获取失败！！')
                    create_branch_time = None

                print('-' * 50 + '开始创建定时任务' + '-' * 50)
                print('序号: ', id)
                print('用户名: ', user_name)
                print('领域名: ', domain_name)
                print('神兵空间英文简称: ', zoneName)
                print('版本名: ', branch)
                print('版本创建时间: ', create_branch_time)
                print('项目ID: ', project_id)
                print('开始时间: ', start_time)
                print('结束时间: ', end_time)
                print('执行任务时间间隔: ', interval_time)
                print('执行任务时间单位: ', time_type)

                if create_branch_time:
                    try:
                        # 添加定时任务
                        if time_type == 'minutes':
                            # 程序中断后重新运行时会自动从数据库读取作业信息，避免重新再添加到调度器中，在 add_job 的参数中增加 replace_existing=True
                            # 想运行错过运行的作业，使用 misfire_grace_time=3600，表示任务只要没有超过3600秒都可以执行，
                            # 如累积多个错过任务，设置 coalesce=True 后，只会执行一次
                            scheduler.add_job(timedTask_move_crads,
                                              args=[user_name, domain_name, zone_name, project_id, branch,
                                                    create_branch_time, ],
                                              trigger='interval',
                                              id=id,
                                              minutes=interval_time,
                                              next_run_time=datetime.datetime.now(),
                                              coalesce=True,
                                              misfire_grace_time=600,
                                              jitter=30,
                                              start_date=start_time,
                                              end_date=end_time,
                                              replace_existing=True)
                        elif time_type == 'hours':
                            scheduler.add_job(timedTask_move_crads,
                                              args=[user_name, domain_name, zone_name, project_id, branch,
                                                    create_branch_time],
                                              trigger='interval',
                                              id=id,
                                              hours=interval_time,
                                              next_run_time=datetime.datetime.now(),
                                              coalesce=True,
                                              misfire_grace_time=3600,
                                              jitter=30,
                                              start_date=start_time,
                                              end_date=end_time,
                                              replace_existing=True)
                        elif time_type == 'days':
                            scheduler.add_job(timedTask_move_crads,
                                              args=[user_name, domain_name, zone_name, project_id, branch,
                                                    create_branch_time],
                                              trigger='interval',
                                              id=id,
                                              days=interval_time,
                                              next_run_time=datetime.datetime.now(),
                                              coalesce=True,
                                              misfire_grace_time=3600,
                                              jitter=30,
                                              start_date=start_time,
                                              end_date=end_time,
                                              replace_existing=True)
                        else:
                            # 理论上不会跑到这里。。。
                            print('创建定时任务失败，执行时间间隔的数据错误！')
                    except Exception as e:
                        print('-' * 50 + '任务创建失败！ starting ' + '-' * 50)
                        print(e)
                        print('-' * 50 + '任务创建失败！ end ' + '-' * 50)

                if scheduler.get_job(job_id=id):
                    TimedTaskForMoveCard.timedTask.filter(id=id).update(taskId=id, taskStatus='生效中',
                                                                        taskObject=scheduler.get_job(job_id=id))
                    print('-' * 50 + '任务id:%s 任务执行中！！' % id + '-' * 50)
                else:
                    getTimedTaskInfo_list = TimedTaskForMoveCard.timedTask.filter(id=id)
                    getTimedTaskInfo_list.delete()
                    print('-' * 50 + '任务已删除' + '-' * 50)
                    print(scheduler.get_job(job_id=id))
                    print('-' * 50 + '任务已删除' + '-' * 50)
            # 删除定时任务
            elif request.POST.get('deletedTimedTask'):
                timedTaskId = request.POST.get('timedTaskId')
                try:
                    scheduler.remove_job(timedTaskId)
                except Exception as e:
                    print('定时任务已超时并自动清除了！')
                _timedTask = TimedTaskForMoveCard.timedTask.filter(id=timedTaskId)
                _timedTask.delete()
            else:
                pass
        ####### 定时任务 end ---- #######

        ####### 任意卡片移动 starting #######
        if myMenu == 'myMenu2':
            if request.POST.get('get_releaseName_cards'):
                any_card_movement_file = 'config/domain_config/any_card_movement_config.ini'
                any_card_movement_config = getConfig(any_card_movement_file)

                if any_card_movement_config.check_key('switch_config', 'switch'):
                    if any_card_movement_config.get_value('switch_config', 'switch') == 'true':
                        whitelist_str = any_card_movement_config.get_value('switch_config', request.session['user_name'])
                        whitelist_str = whitelist_str.replace(' ', '')
                        whitelist_str = whitelist_str.replace('，', ',')
                        whitelist = whitelist_str.split(',')

                        # 获取该用户下的所有领域名
                        domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
                        read_domain = getConfig(domain_file)
                        domain_list = read_domain.get_section()
                        try:
                            domain = read_domain.get_value(domain_name, 'domain_name_management')  # 获取神兵空间简称
                            # print('获取神兵空间简称: ', domain)
                        except:
                            domain = None

                        if domain in whitelist:
                            wizardGlobalId_list = request.POST.getlist('cardID')
                            stateDetail = request.POST.get('card_status_name_list')

                            move_cards_myMenu2 = []  # 储存修改状态成功的卡片
                            unmove_cards_myMenu2 = []  # 储存修改状态失败的卡片

                            for wizardGlobalId in wizardGlobalId_list:
                                status_code = modify_card_state(wizardGlobalId, stateDetail)
                                if len(status_code) == 1:
                                    move_cards_myMenu2.append(wizardGlobalId)
                                else:
                                    unmove_cards_myMenu2.append(wizardGlobalId)

                # wizardGlobalId_list=request.POST.getlist('cardID')
                # stateDetail=request.POST.get('card_status_name_list')
                #
                # move_cards_myMenu2=[]   # 储存修改状态成功的卡片
                # unmove_cards_myMenu2=[] # 储存修改状态失败的卡片
                #
                # for wizardGlobalId in wizardGlobalId_list:
                #     status_code=modify_card_state(wizardGlobalId,stateDetail)
                #     if len(status_code) == 1:
                #         move_cards_myMenu2.append(wizardGlobalId)
                #     else:
                #         unmove_cards_myMenu2.append(wizardGlobalId)
        ####### 任意卡片移动 end ---- #######

    # 获取用户下所有的定时任务列表
    loginUser = request.session['user_name']

    getDomainTimedTask_list = TimedTaskForMoveCard.timedTask.filter(userName=loginUser, domainName=domain_name).order_by(
        'id')
    print('-' * 50 + ' 当前领域定时任务列表 starting ' + '-' * 50)
    print('getDomainTimedTask_list: ', getDomainTimedTask_list)
    for domainTimedTask in getDomainTimedTask_list:
        print(domainTimedTask.id)
        print(domainTimedTask.projectId)
        print(domainTimedTask.branch)
        print(domainTimedTask.startTime)
        print(domainTimedTask.endTime)
        print(domainTimedTask.intervalTime)
        print(domainTimedTask.taskStatus)
    print('-' * 50 + ' 当前领域定时任务列表 end ' + '-' * 50)

    # 获取该用户下的所有领域名
    domain_file = 'config/domain_config/%s_domain_config.ini' % request.session['user_name']
    read_domain = getConfig(domain_file)
    domain_list = read_domain.get_section()
    try:
        domain = read_domain.get_value(domain_name, 'domain_name_management')  # 获取神兵空间简称
        # print('获取神兵空间简称: ',domain)
    except:
        domain = None
    try:
        projectid_str = read_domain.get_value(domain_name, 'projectid')  # 获取项目ID列表
        projectid_list = projectid_str.split(',')
    except:
        projectid_str = None
        projectid_list = []

    try:
        privatekey = read_domain.get_value(domain_name, 'privatekey')  # 获取gitlab访问令牌privatekey
    except:
        privatekey = None

    # 神兵空间简称不为None时
    if domain:
        # 获取神兵空间版本及版本的创建时间
        releaseName_info = get_releaseName_info(domain)
        releaseName_respone = releaseName_info.request()
        releaseName_dict, planReleaseEndDate_dict = releaseName_info.get_releaseName(releaseName_respone)
        print('未投产的版本号:  ', releaseName_dict)
        print('版本的投产日期:  ', planReleaseEndDate_dict)

        releaseName_list = []  # 储存排列后的分支
        # 当领域不为None时
        if releaseName_dict:
            new_releaseName_dict = {}
            for releaseName, createdDate in releaseName_dict.items():
                # 匹配有中文的字符串
                matchStr = re.findall('[\u4e00-\u9fff]', releaseName, re.M | re.I | re.S)
                if len(matchStr) == 0:
                    new_releaseName_dict[releaseName] = createdDate
            # 按key降序排列
            new_releaseName_list = sorted(new_releaseName_dict.items(), reverse=True)
            # 获取第一个key值，即列表中第一个分支的创建时间

            # 当神兵空间存在版本时
            if new_releaseName_list:
                createdDate = new_releaseName_list[0][1]
                # print('当前创建分支时间createdDate：',createdDate)
                new_releaseName_dict = dict(new_releaseName_list)
                # print('new_releaseName_dict排列之后: ', new_releaseName_dict)

                branch_file = 'config/domain_config/%s_branch_config.ini' % request.session['user_name']
                if os.path.exists(branch_file):
                    print(request.session['user_name'], '文件已存在，不需要创建!')
                else:
                    with open(branch_file, 'a+') as f:
                        print(request.session['user_name'], '文件不存在,新建新文件!')

                # 添加节点
                add_config = getConfig(branch_file)
                if add_config.check_section(domain_name):
                    pass
                else:
                    add_config.add_section(domain_name)

                for releaseName_tmp, createdDate_tmp in new_releaseName_dict.items():
                    # 获取分支
                    releaseName_list.append(releaseName_tmp)
                    # 添加节点数据
                    add_config.set_section(domain_name, releaseName_tmp, createdDate_tmp)
                add_config.save()

                # 选择分支时，设置页面默认分支为该分支
                if request.POST.get('select_branch'):
                    branch = request.POST.get('select_branch')
                    releaseName_list.remove(branch)
                    releaseName_list.insert(0, branch)
                    createdDate = add_config.get_value(domain_name, branch)

                if request.POST.get('branch'):
                    branch = request.POST.get('branch')
                    releaseName_list.remove(branch)
                    releaseName_list.insert(0, branch)
                    get_config = getConfig(branch_file)
                    createdDate = get_config.get_value(request.POST.get('domain_name'), branch)
                    # print('当前移动卡片分支为：', branch)
                    # print('当前分支创建时间：：', createdDate)
                    # print('当前所有分支releaseName_list：', releaseName_list)

                    projectid_select = request.POST.getlist('projectId')
                    for id in projectid_select:
                        projectid_list.remove(id)
                    # print('projectid_select被选中的项目ID: ', projectid_select)
                    # print('projectid_list去除被选中后的项目ID: ', projectid_list)

                createdDate = createdDate[:-3]
                createdDate = createdDate.replace(" ", "T")
                # print('createdDate: ',createdDate)
                print(releaseName_list)

        if planReleaseEndDate_dict:
            planReleaseInfo_file = 'config/domain_config/%s_planReleaseInfo_config.ini' % request.session['user_name']
            if os.path.exists(planReleaseInfo_file):
                print(request.session['user_name'], '文件已存在，不需要创建!')
            else:
                with open(planReleaseInfo_file, 'a+') as f:
                    print(request.session['user_name'], '文件不存在,新建新文件!')

            # 添加版本计划信息
            planReleaseInfo_config = getConfig(planReleaseInfo_file)
            if planReleaseInfo_config.check_section(domain_name):
                print(planReleaseInfo_config.check_section(domain_name))
            else:
                planReleaseInfo_config.add_section(domain_name)

            for planRelease, endDate in planReleaseEndDate_dict.items():
                planReleaseInfo_config.set_section(domain_name, planRelease, endDate)
            planReleaseInfo_config.save()

            try:
                # 获取第一个版本的投产日期，用于显示在定时移动卡片中的结束时间输入框
                TimedTask_endDate = planReleaseInfo_config.get_value(domain_name, releaseName_list[0])
                TimedTask_endDate = TimedTask_endDate[:-3]
                TimedTask_endDate = TimedTask_endDate.replace(" ", "T")
            except Exception as e:
                print(e)
                TimedTask_endDate = None

            ###### 用于任意卡片移动功能 starting ######
            any_card_movement_file = 'config/domain_config/any_card_movement_config.ini'
            if os.path.exists(any_card_movement_file):
                print(any_card_movement_file, '文件已存在，不需要创建!')
            else:
                with open(any_card_movement_file, 'a+') as f:
                    print(any_card_movement_file, '文件不存在,新建新文件!')

            any_card_movement_config = getConfig(any_card_movement_file)

            if any_card_movement_config.check_section('switch_config'):
                print(any_card_movement_config.check_section('switch_config'))
            else:
                any_card_movement_config.add_section('switch_config')
                any_card_movement_config.set_section('switch_config', 'switch', 'false')
                any_card_movement_config.save()

            if any_card_movement_config.check_key('switch_config', 'switch'):
                if any_card_movement_config.get_value('switch_config', 'switch') == 'true':
                    try:
                        whitelist_str = any_card_movement_config.get_value('switch_config', request.session['user_name'])
                        whitelist_str = whitelist_str.replace(' ', '')
                        whitelist_str = whitelist_str.replace('，', ',')
                        whitelist = whitelist_str.split(',')
                        # print('whitelist: ',whitelist)
                        # print('神兵空间简称domain: ',domain)

                        if domain in whitelist:
                            # 从神兵获取用户故事和缺陷的所有泳道名称
                            card_status_name_list = get_cards_status_name(domain)
                            # 获取第一个版本的用户故事卡片和缺陷卡片
                            defect_and_story_cards_dict = get_defect_and_story_cards(domain, releaseName_list[0])
                        else:
                            defect_and_story_cards_dict = None
                            any_card_movement_message = '此空间未加入白名单，不符合条件使用该功能！'
                    except Exception as e:
                        print(e)
                        defect_and_story_cards_dict = None
                        any_card_movement_message = '此空间未加入白名单或没有版本计划，不符合条件使用该功能，请联系管理员！'
                else:
                    defect_and_story_cards_dict = None
                    any_card_movement_message = '功能总开关未开启，请联系管理员打开总开关再使用！'
            else:
                defect_and_story_cards_dict = None
                any_card_movement_message = '功能总开关不存在，不符合条件使用该功能！'
            ###### 用于任意卡片移动功能 end --- ######

        else:
            ###### 用于任意卡片移动功能 starting ######
            defect_and_story_cards_dict = None
            any_card_movement_message = '此空间没有版本计划，不符合条件使用该功能！'
            ###### 用于任意卡片移动功能 end --- ######

    # 当前时间
    now_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    # 当前日期,用在定时移动卡片起始时间
    now_date = datetime.datetime.now().strftime("%Y-%m-%dT00:00")

    if myMenu == 'myMenu0':
        myMenu0 = 'select'
    elif myMenu == 'myMenu1':
        myMenu1 = 'select'
    elif myMenu == 'myMenu2':
        myMenu2 = 'select'
    elif myMenu == 'myMenu3':
        myMenu3 = 'select'
    else:
        myMenu0 = 'select'
    return render(request, 'software/modifyCardStatus.html', locals())


def interfacePerson(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(interfacePerson.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request, 'software/interfacePerson.html', locals())


def announcement(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(announcement.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【生产数据库信息】请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == "POST":
        if request.POST.get('operating') == 'deleted':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                modifyTime = request.POST.get('modifyTime')
                prdDataBase = PrdDataBaseInfo.prddatabase.filter(loginUser=loginUser, id=id,
                                                                 modifyTime=modifyTime, envType='prd')
                prdDataBase.delete()
                # print('%s删除成功！'%prdDataBase)
        else:
            newPrdDataBase = PrdDataBaseInfo.prddatabase.create()
            newPrdDataBase.loginUser = request.session['user_name']
            newPrdDataBase.blongTo = request.POST.get('blongTo').replace(" ", "")
            newPrdDataBase.domain = request.POST.get('domain').replace(" ", "")
            newPrdDataBase.dataBaseLink = request.POST.get('dataBaseLink').replace(" ", "")
            newPrdDataBase.dataBaseName = request.POST.get('dataBaseName').replace(" ", "")
            newPrdDataBase.userName = request.POST.get('userName').replace(" ", "")
            newPrdDataBase.remark = request.POST.get('remark').replace(" ", "")
            newPrdDataBase.envType = 'prd'
            newPrdDataBase.modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            newPrdDataBase.save()
    try:
        # 从数据库中查询当前登录用户的解封版所收集的信息
        prdDataBaseInfo_list = PrdDataBaseInfo.prddatabase.filter(loginUser=request.session['user_name'],
                                                                  envType='prd').order_by('-id')
        blongTo_list = []
        for prdDataBaseInfo in prdDataBaseInfo_list:
            # print(prdDataBaseInfo.blongTo)
            blongTo_list.append(prdDataBaseInfo.blongTo)
            # print('去重前列表：', blongTo_list)
        blongTo_list = list(set(blongTo_list))
        # print('去重后列表：', blongTo_list)

        all_blongTo_dict = {}
        for blongTo in blongTo_list:
            same_blongTo_list = []
            for prdDataBaseInfo in prdDataBaseInfo_list:
                if prdDataBaseInfo.blongTo == blongTo:
                    same_blongTo_list.append(prdDataBaseInfo)
            all_blongTo_dict[blongTo] = same_blongTo_list
        # print('all_blongTo_dict: ',all_blongTo_dict)

    except Exception as e:
        print(e)
        print('此用户没有生产数据库信息！')
    return render(request, 'software/announcement.html', locals())


def setUpCollectionMaterialConfig(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(setUpCollectionMaterialConfig.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【设置检查项】请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == "POST":
        if not request.session.get('manager_islogin', None):
            message = "您尚未登录超级用户，请先登录！！"
        else:
            domain = request.POST.get('domain')
            checkout_list = request.POST.getlist('checkout_list')
            report_check_config = getConfig('config/software_config/report_check_list_config.ini')
            if checkout_list:
                checkout_str = ",".join(str(i) for i in checkout_list)  # 将list转成字符串，中间用符号分隔
                # 保存，写入到配置文件
                report_check_config.set_section('report_check_list', domain, checkout_str)
                message = "设置 %s 领域成功！" % domain
            else:
                # 删除key
                report_check_config.remove_key('report_check_list', domain)
                message = "删除 %s 领域成功！" % domain
            report_check_config.save()

    user_management_config = getConfig('config/software_config/user_management_config.ini')
    # 获取 目录下不显示上传功能的黑名单
    black_user_list = user_management_config.get_value('user_list', 'black_user_list').split(',')
    # 获取 可访问投产材料管理页面的白名单
    allow_users_list = user_management_config.get_value('user_list', 'allow_users_list').split(',')

    if request.session['user_name'] in black_user_list and request.session['user_name'] in allow_users_list:
        user_home = 'uploads/' + request.session['user_name'] + '/'
        fileList = os.listdir(user_home)
        domain_list = []
        for file in fileList:
            if os.path.isdir(user_home + file):
                domain_list.append(file.split("（")[0])  # 获取该用户下的所有领域
        try:
            domain_list.remove('1-版本检查单')
        except:
            pass
        # print('该用户下的所有领域: ',domain_list)

        report_check_config = getConfig('config/software_config/report_check_list_config.ini')
        check_type_list = report_check_config.get_value('report_check_list', 'ALL')  # 获取需要检查的所有报告
        check_type_list = check_type_list.split(',')  # 字符串转成列表数据类型
        # print('获取需要检查的所有报告: ',check_type_list)

        domain_report_dict = {}
        for domain in domain_list:  # 获取本地每个领域需要检查的报告
            domain_report_list = []
            try:
                check_type_list_temp = report_check_config.get_value('report_check_list', domain)
                check_type_list_temp = check_type_list_temp.split(',')
                for check_type in check_type_list:
                    if check_type in check_type_list_temp:
                        domain_report_list.append('✔')
                    else:
                        domain_report_list.append('不涉及')
            except:
                for check_type in check_type_list:
                    domain_report_list.append('未设置')
            domain_report_dict[domain] = domain_report_list  # 把本地每个领域检查项是否存在结果保存下来

        return render(request, 'software/setUpCollectionMaterialConfig.html', locals())
    else:
        return render(request, 'software/ERROR.html', locals())


def downloadByClassification(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(downloadByClassification.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    try:
        '''分类打包下载文件，只适用于上传文件检查投产材料页面'''
        # source_dir='uploads/shar/BRON-CLSS（车主生活服务子系统）/BRON-CLSS1.7.0（2020-09-10）'
        source_dir = request.GET.get('source_dir')

        # source_dir='uploads/shar/BRON-CLSS（车主生活服务子系统）/BRON-CLSS1.7.0（2020-09-10）'
        if source_dir[-1] == '/':
            source_dir = source_dir[:-1]

        # BRON-CLSS
        domain_name = source_dir.split('/')[2].split('（')[0]

        '''文件分类 starting'''
        # 获取版本号,BRON-COSS1.2.0
        version = source_dir.split('/')[3].split('（')[0]
        if version is None:
            version = domain_name

        # 获取版本号带日期，BRON-COSS1.2.0（2020-10-30）
        planName_data = source_dir.split('/')[-1]
        # print('带版本日期：', planName_data)
        if planName_data is None:
            planName_data = domain_name

        # 获取所有文件名
        file_list = os.listdir(source_dir)
        for file in file_list:
            if os.path.isdir(source_dir + "/" + file):
                file_list.remove(file)  # 去除子目录

        file_list_temp = os.listdir(source_dir)
        # print('file_list_temp原始数据：',file_list_temp)
        logging.info('INFO：file_list_temp原始数据: ', file_list_temp)
        for file in file_list_temp:
            if os.path.isdir(source_dir + "/" + file):
                file_list_temp.remove(file)  # 去除子目录

        if len(file_list) == 0:
            return False
    except Exception as e:
        print(e)
        logging.info('ERROR：%s' % e)
        return render(request, 'software/ERROR.html', locals())

    getMatchKeywords = getConfig('config/software_config/report_check_list_config.ini')

    # 获取所有检查报告，不分前后端
    all_check_report = getMatchKeywords.get_value('all_report_check', 'all_report')
    # 去空格
    all_check_report = all_check_report.strip()
    # 把字符串(配置)转换为列表
    all_check_report = all_check_report.split(',')

    try:
        # 获取领域所需要检查的报告
        domain_check_report = getMatchKeywords.get_value('report_check_list', domain_name)
        # 去空格
        domain_check_report = domain_check_report.strip()
        # 把字符串(配置)转换为列表
        domain_check_report = domain_check_report.split(',')
    except Exception as e:
        print(e)
        return render(request, 'software/warn.html')

    # 不涉及的检查报告
    uncheck_report = list(set(all_check_report).difference(set(domain_check_report)))
    print('不涉及的检查报告: ', uncheck_report)

    print('---------------------------------------------------')
    print('%s检查报告列表：%s' % (domain_name, all_check_report))
    print('---------------------------------------------------')

    # 创建临时目录
    tempDir = planName_data + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%H%S')
    tempDir = tempDir.replace(' ', '')
    targetPath = 'uploads' + '/' + 'temp'

    # uploads/temp/BRON-CLSS1.7.0（2020-09-10）_20201105113012123456/BRON-CLSS1.7.0（2020-09-10）
    sourcePath = targetPath + '/' + tempDir + '/' + planName_data
    # 创建打包临时目录
    os.makedirs(sourcePath)
    # print('创建分类zip打包临时目录：',sourcePath)

    i = 1
    all_repoty_dir_name = []  # 存放创建分类目录名称
    for report in all_check_report:
        # 创建分类目录
        # print('创建分类目录：',sourcePath + '/' + report)
        report_dir_temp = sourcePath + '/' + str(i) + '.' + report
        os.mkdir(report_dir_temp)
        all_repoty_dir_name.append(report_dir_temp)
        i += 1
        # findStr = getMatchKeywords.get_value('match_keywords', report)
        # print('%s 的匹配关键字：'%report,findStr)
        try:
            findStr = getMatchKeywords.get_value('match_keywords', report)
            # print('%s 的匹配关键字：'%report,findStr)
        except Exception as e:
            print(e)
            # print('本次匹配没有匹配到对应的报告类型！')
            continue

        # print('file_list所有文件列表：',file_list)
        logging.info('INFO：file_list所有文件列表: ', file_list)
        for file in file_list:
            matchStr = re.findall(findStr, str(file), re.M | re.I | re.S)
            if matchStr:
                # print('拷贝目标路径: ',file_path+'/'+str(file),sourcePath+'/'+report+'/'+str(file))
                # 拷贝文件和状态信息
                shutil.copy2(source_dir + '/' + str(file), report_dir_temp + '/' + str(file))
                # print('【%s】报告已拷贝到【%s】目录！' % (file, report))
                logging.info('INFO：【%s】报告已拷贝到【%s】目录！' % (file, report))
                # logging.info('INFO：file_list_temp: ',file_list_temp)
                # print('file_list_temp: ',file_list_temp)
                try:
                    file_list_temp.remove(file)
                except Exception as e:
                    print('file_list_temp列表移除名称有误: ', e)
                    logging.info('ERROR：file_list_temp列表移除名称有误: ', e)

        if report in uncheck_report:
            # print('当文件夹为空目录时:表明不涉及此项 ')
            if not os.listdir(report_dir_temp):
                with open(report_dir_temp + '/' + "不涉及此项.txt", 'w+') as f:
                    f.write("不涉及")
    else:
        os.mkdir(sourcePath + '/' + str(i) + '.' + '其他')
        with open(sourcePath + '/' + str(i) + '.' + '其他' + '/' + "None.txt", 'w+') as f:
            f.write("None")
        # print('创建分类目录：', sourcePath + '\\' + '其他')

    for report_dir_name in all_repoty_dir_name:
        # print('当文件夹为空目录时表明没有收集到报告 ')
        if not os.listdir(report_dir_name):
            with open(report_dir_name + '/' + "None.txt", 'w+') as f:
                f.write("None")

    for file in file_list_temp:
        shutil.copy2(source_dir + '/' + str(file), sourcePath + '/' + str(i) + '.' + '其他' + '/' + str(file))
        # print('【%s】报告已拷贝到【其他】目录！' % file)

    '''文件分类 end'''

    '''打包--未加密 starting'''
    source_dir = sourcePath
    output_dir = targetPath
    output_filename = planName_data + '.zip'
    make_zip(source_dir, output_dir, output_filename)
    '''打包--未加密 end'''

    try:
        # 删除临时目录
        shutil.rmtree(targetPath + '/' + tempDir)
        # print('删除临时目录成功：', targetPath + '/' + tempDir)
        logging.info('INFO：删除临时目录成功：%s/%s' % (targetPath, tempDir))
    except Exception as e:
        # print('删除临时目录失败：',targetPath + '/' + tempDir)
        logging.info(' ERROR：删除临时目录失败：', targetPath + '/' + tempDir)

    # '''打包 starting'''
    # outFullName=sourcePath+planName_data'+'.zip'
    # password='123'
    # isSuccessful = zipDir(sourcePath, outFullName, password)
    # if isSuccessful == True:
    #     print('zip打包成功！' )
    # else:
    #     print('zip打包失败！')
    # '''加密打包 end'''
    print(output_dir + '/' + output_filename)
    return downloadFile(request, output_dir + '/' + output_filename)


def get_access_level(number):
    # 通过数字获取gitlab访问等级名称
    if number == 10:
        return 'Guest'
    elif number == 15:
        return 'RoleManager'
    elif number == 20:
        return 'Reporter'
    elif number == 30:
        return 'Developer'
    elif number == 35:
        return 'Auditor'
    elif number == 36:
        return 'ProjectManager'
    elif number == 40:
        return 'Maintainer'
    elif number == 50:
        return 'Owner'
    else:
        return '访问权限等级不存在！'


def gitlab_member_permissions(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(gitlab_member_permissions.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))


    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【gitlab权限管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您尚未登录超级用户，请先登录！！"
        return render(request, 'software/index.html', locals())

    # 获取GET请求时停留在哪个功能页面
    if request.GET.get('feature'):
        myMenu = request.GET.get('feature')
        # print('myMenu: ', myMenu)
    # 获取POST请求时停留在哪个功能页面
    elif request.POST.get('feature'):
        myMenu = request.POST.get('feature')
        # print('当前菜单位置: ', myMenu)
    else:
        myMenu = 'myMenu0'

    userInfo_file = 'config/domain_config/userInfo_config.ini'
    if os.path.exists(userInfo_file):
        # print('%s文件已存在，不需要创建!' % userInfo_file)
        pass
    else:
        with open(userInfo_file, 'a+') as f:
            # print('%s文件不存在,新建新文件!' % userInfo_file)
            pass

    if request.method == 'POST':
        ###### 更新用户个人访问令牌，此令牌一般为gitlab Owner权限 starting ######
        if request.POST.get('updatePrivateKey') == 'updatePrivateKey':
            privateKey = request.POST.get('privateKey')

            userInfo_config = getConfig(userInfo_file)
            if userInfo_config.check_section('userPrivateKey'):
                print(userInfo_config.check_section('userPrivateKey'))
            else:
                userInfo_config.add_section('userPrivateKey')

            userInfo_config.set_section('userPrivateKey', request.session['user_name'], privateKey)
            userInfo_config.save()
            message = "访问令牌更新成功！"
        ###### 更新用户个人访问令牌，此令牌一般为gitlab Owner权限 end ---- ######

        ###### 添加gitlab权限 starting ######
        if request.POST.get('addPremissions') == 'addPremissions':
            userInfo_config = getConfig(userInfo_file)
            privateKey = userInfo_config.get_value('userPrivateKey', request.session['user_name'])
            projectsType = request.POST.get('projectsType')

            projectId_str = request.POST.get('projectId')
            projectId_str = projectId_str.replace(" ", "")  # 去空格
            projectId_str = projectId_str.replace("，", ",")  # 中文逗号转英文逗号
            projectId_list = projectId_str.split(",")  # 分割
            projectId_list = [x for x in projectId_list if x != '']  # 列表去空值

            member_str = request.POST.get('member')
            member_str = member_str.replace(" ", "")  # 去空格
            member_str = member_str.replace("，", ",")  # 中文逗号转英文逗号
            member_list = member_str.split(",")
            member_list = [x for x in member_list if x != '']  # 列表去空值

            # 获取权限
            permissions = request.POST.get('permissions')
            # Guest 10 => Guest access
            # RoleManager 15
            # Reporter 20 => Reporter access
            # Developer 30 => Developer access
            # Auditor 35
            # ProjectManager 36
            # Maintainer 40 => Maintainer access
            # Owner 50 => Owner access # Only valid for groups

            # 获取权限到期日期
            expires_at = request.POST.get('end_date')

            # 这里获取用户ID只需要正确的访问令牌和UM账号即可，所以前面两个传参随意填写也行
            get_gitlab_api = request_gitlab_api('project_id', 'service_name', privateKey)

            member_id_dict = {}  # 获取存在的用户ID
            add_member_id_is_None_list = []  # 获取用户ID失败的用户名
            for member in member_list:
                member_id = get_gitlab_api.get_user_id(member)  # 根据UM账号获取用户ID
                if member_id:
                    member_id_dict[member] = member_id
                else:
                    add_member_id_is_None_list.append(member)

            # print('查询到的所有用户ID：',member_id_dict)

            if member_id_dict:
                resultInfo_list = []
                result = None
                for member, member_id in member_id_dict.items():
                    # print('member: ',member)
                    # print('member_id: ',member_id)
                    for projectid_temp in projectId_list:
                        # 如果调用接口用户有权限，返回结果不为空，否则为空
                        result = get_gitlab_api.add_member_permissions(projectsType, projectid_temp, member_id, permissions, expires_at)
                        resultInfo_list.append({"%s（%s）" % (member, projectid_temp): result})
                # print('resultInfo_list: ',resultInfo_list)

                new_add_resultInfo_list = []
                number = 0
                for accessInfo_dict in resultInfo_list:
                    number += 1
                    for userName, accessInfo in accessInfo_dict.items():
                        if accessInfo:
                            try:
                                new_add_resultInfo_list.append(
                                    {userName: {'number': number, 'message': "添加失败，%s" % accessInfo['message']}})
                            except Exception as e:
                                access_level = accessInfo['access_level']
                                access_level = get_access_level(accessInfo['access_level'])
                                # print('序号：',number)
                                # print('项目ID：',number)
                                # print('UM账号：',userName)
                                # print('授权等级：',access_level)
                                # print('到期日期：',accessInfo['expires_at'])
                                # print('-'*50)
                                new_add_resultInfo_list.append(
                                    {userName: {'number': number, 'access_level': access_level,
                                                'expires_at': accessInfo['expires_at'], 'message': "添加成功!"}})
                        else:
                            new_add_resultInfo_list.append(
                                {userName: {'number': number, 'message': "添加失败，用户可能无权限添加，请确保访问令牌有Owner权限！"}})
                    # print('new_add_resultInfo_list: ', new_add_resultInfo_list)
        ###### 添加gitlab权限 end ######

        ###### 修改gitlab权限 starting ######
        if request.POST.get('updatePremissions') == 'updatePremissions':
            userInfo_config = getConfig(userInfo_file)
            privateKey = userInfo_config.get_value('userPrivateKey', request.session['user_name'])
            projectsType = request.POST.get('projectsType')

            projectId_str = request.POST.get('projectId')
            projectId_str = projectId_str.replace(" ", "")  # 去空格
            projectId_str = projectId_str.replace("，", ",")  # 中文逗号转英文逗号
            projectId_list = projectId_str.split(",")  # 分割
            projectId_list = [x for x in projectId_list if x != '']  # 列表去空值

            member_str = request.POST.get('member')
            member_str = member_str.replace(" ", "")  # 去空格
            member_str = member_str.replace("，", ",")  # 中文逗号转英文逗号
            member_list = member_str.split(",")
            member_list = [x for x in member_list if x != '']  # 列表去空值

            # 获取权限
            permissions = request.POST.get('permissions')
            # Guest 10 => Guest access
            # RoleManager 15
            # Reporter 20 => Reporter access
            # Developer 30 => Developer access
            # Auditor 35
            # ProjectManager 36
            # Maintainer 40 => Maintainer access
            # Owner 50 => Owner access # Only valid for groups

            # 获取权限到期日期
            expires_at = request.POST.get('end_date')

            # 这里获取用户ID只需要正确的访问令牌和UM账号即可，所以前面两个传参随意填写也行
            get_gitlab_api = request_gitlab_api('project_id', 'service_name', privateKey)

            member_id_dict = {}  # 获取存在的用户ID
            modify_member_id_is_None_list = []  # 获取用户ID失败的用户名
            for member in member_list:
                member_id = get_gitlab_api.get_user_id(member)  # 根据UM账号获取用户ID
                if member_id:
                    member_id_dict[member] = member_id
                else:
                    modify_member_id_is_None_list.append(member)
            # print('查询到的所有用户ID：',member_id_dict)

            if member_id_dict:
                resultInfo_list = []
                for member, member_id in member_id_dict.items():
                # print('member: ',member)
                # print('member_id: ',member_id)
                    for projectid_temp in projectId_list:
                        result = get_gitlab_api.update_member_permissions(projectsType, projectid_temp, member_id, permissions, expires_at)
                        resultInfo_list.append({"%s（%s）" % (member, projectid_temp): result})
                # print('resultInfo_list: ',resultInfo_list)

                new_modify_resultInfo_list = []
                number = 0
                for accessInfo_dict in resultInfo_list:
                    number += 1
                    for userName, accessInfo in accessInfo_dict.items():
                        try:
                            new_modify_resultInfo_list.append({userName: {'number': number, 'message': "修改失败，%s" % accessInfo['message']}})
                        except Exception as e:
                            access_level = accessInfo['access_level']
                            access_level = get_access_level(accessInfo['access_level'])
                            # print('序号：',number)
                            # print('UM账号：',userName)
                            # print('授权等级：',access_level)
                            # print('到期日期：',accessInfo['expires_at'])
                            # print('-'*50)
                            new_modify_resultInfo_list.append({userName: {'number': number, 'access_level': access_level,
                                                                          'expires_at': accessInfo['expires_at'], 'message': "修改成功!"}})
                # print('new_modify_resultInfo_list: ', new_modify_resultInfo_list)
        ###### 修改gitlab权限 end ---- ######

        ###### 删除gitlab权限 starting ######
        if request.POST.get('deletePremissions') == 'deletePremissions':
            userInfo_config = getConfig(userInfo_file)
            privateKey = userInfo_config.get_value('userPrivateKey', request.session['user_name'])
            projectsType = request.POST.get('projectsType')

            projectId_str = request.POST.get('projectId')
            projectId_str = projectId_str.replace(" ", "")  # 去空格
            projectId_str = projectId_str.replace("，", ",")  # 中文逗号转英文逗号
            projectId_list = projectId_str.split(",")  # 分割
            projectId_list = [x for x in projectId_list if x != '']  # 列表去空值

            member_str = request.POST.get('member')
            member_str = member_str.replace(" ", "")  # 去空格
            member_str = member_str.replace("，", ",")  # 中文逗号转英文逗号
            member_list = member_str.split(",")
            member_list = [x for x in member_list if x != '']  # 列表去空值

            # 这里获取用户ID只需要正确的访问令牌和UM账号即可，所以前面两个传参随意填写也行
            get_gitlab_api = request_gitlab_api('project_id', 'service_name', privateKey)

            member_id_dict = {}  # 获取存在的用户ID
            del_member_id_is_None_list = []  # 获取用户ID失败的用户名
            for member in member_list:
                member_id = get_gitlab_api.get_user_id(member)  # 根据UM账号获取用户ID
                if member_id:
                    member_id_dict[member] = member_id
                else:
                    del_member_id_is_None_list.append(member)
            # print('查询到的所有用户ID：',member_id_dict)

            if member_id_dict:
                resultInfo_list = []
                for member, member_id in member_id_dict.items():
                    # print('member: ',member)
                    # print('member_id: ',member_id)
                    for projectid_temp in projectId_list:
                        result = get_gitlab_api.delete_member_permissions(projectsType, projectid_temp, member_id)
                        resultInfo_list.append({"%s（%s）" % (member, projectid_temp): result})
                # print('resultInfo_list: ',resultInfo_list)

                new_del_resultInfo_list = []
                number = 0
                for accessInfo_dict in resultInfo_list:
                    number += 1
                    for userName, accessInfo in accessInfo_dict.items():
                        try:
                            if not accessInfo:
                                new_del_resultInfo_list.append({userName: {'number': number, 'message': '删除成功!'}})
                            else:
                                accessInfo = eval(accessInfo)
                                new_del_resultInfo_list.append({userName: {'number': number, 'message': "删除失败，%s" % accessInfo['message']}})
                        except Exception as e:
                            # print(e)
                            new_del_resultInfo_list.append({userName: {'number': number, 'message': "删除失败，%s" % e}})
                # print('new_del_resultInfo_list: ', new_del_resultInfo_list)
        ###### 删除gitlab权限 end ---- ######

    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    expires_at_date = datetime.datetime.now().strftime("%Y-10-31")
    get_userInfo_config = getConfig(userInfo_file)
    try:
        privateKey = get_userInfo_config.get_value('userPrivateKey', request.session['user_name'])
    except Exception as e:
        print(e)
        print('没有找到当前用户【%s】个人访问令牌privateKey' % request.session['user_name'])
        logging.info(("WARN：没有找到当前用户【%s】个人访问令牌privateKey" % request.session['user_name']))

    return render(request, 'software/gitlab_member_permissions.html', locals())


# 添加神兵空间卡片自定义字段
def add_card_Field(projectAbbrName, customFieldName, customFieldType, customFieldSubjectTypes, customFieldConfig=None):
    url = 'http://wb-pab.paic.com.cn/api/service'
    userToken = 'f33e4f72-cc8d-4e14-8449-774a6293039a'
    serviceName = 'alm.project.customField.create'

    params = {
        'projectAbbrName': projectAbbrName,
        'customFieldName': customFieldName,
        'customFieldType': customFieldType,
        'customFieldSubjectTypes': customFieldSubjectTypes
    }

    if customFieldConfig:
        params['customFieldConfig'] = customFieldConfig

    logging.info('INFO：添加神兵空间自定义字段的参数如下：%s' % params)
    respone = request(url, userToken, serviceName, params).run()
    # print(respone.json())
    return respone


def addCardField(request):
    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【添加神兵空间字段】请先登录！！"
        return render(request, 'software/index.html', locals())

    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您尚未登录超级用户，请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == 'POST':
        fieldName = request.POST.get('fieldName')  # 获取字段名称
        customFieldType = request.POST.get('select_menu')  # 获取复选框选项
        customFieldSubjectTypes_list = request.POST.getlist('customFieldSubjectTypes')  # 获取自定义字段应用到哪些类型中
        customFieldSubjectTypes = ','.join(customFieldSubjectTypes_list)

        domain_list = request.POST.getlist('domain')  # 获取领域名
        singlechoice_list = request.POST.getlist('singlechoice')  # 获取下拉框选项
        multiplechoice_list = request.POST.getlist('multiplechoice')  # 获取复选框选项

        fieldName = fieldName.replace(" ", "")  # 字符串去空值
        domain_list = [x for x in domain_list if x != '']  # 列表去空值
        singlechoice_list = [x for x in singlechoice_list if x != '']  # 列表去空值
        multiplechoice_list = [x for x in multiplechoice_list if x != '']  # 列表去空值
        customFieldType = customFieldType.replace(" ", "")  # 字符串去空值
        customFieldType = customFieldType.upper()  # 把所有字符中的小写字母转换成大写字母

        if singlechoice_list and multiplechoice_list:
            message = "下拉框和复选框不允许同时填写内容，请重新填写！"
            return render(request, 'software/addCardField.html', locals())

        if customFieldType == "SINGLECHOICE":
            customFieldConfig = ','.join(singlechoice_list)
        elif customFieldType == "MULTIPLECHOICE":
            customFieldConfig = ','.join(multiplechoice_list)
        else:
            customFieldConfig = None

        success_message_list = []
        fail_message_list = []
        for domain in domain_list:
            try:
                respone = add_card_Field(domain, fieldName, customFieldType, customFieldSubjectTypes, customFieldConfig)
                logging.info('INFO：添加神兵空间自定义返回信息如下：%s' % respone.json())
                if respone.json()['header']['ret'] == 0:
                    success_message_list.append(domain)
                else:
                    fail_message_list.append(domain)
            except Exception as e:
                fail_message_list.append(domain)
                logging.info('ERROR：添加神兵空间自定义字段错误：', e)
    return render(request, 'software/addCardField.html', locals())


def countDeploymentInfo(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【部署窗口申请】请先登录！！"
        return render(request, 'software/index.html', locals())

    countDeploymentInfo_file = 'config/domain_config/countDeploymentInfo_config.ini'
    if not os.path.exists(countDeploymentInfo_file):
        with open(countDeploymentInfo_file, 'a+') as f:
            pass

    deploymentInfo = getConfig(countDeploymentInfo_file)

    if request.session.get('manager_islogin', None):
        isWorkTime = True  # 当用户是超级管理时，则把当前时间看作工作时间
        isWorkTime_mark = False  # 当用户是超级管理时，同时看作非工作时间
    else:
        # april_last = datetime.datetime(2021, 12, 31, 9, 59,15)
        april_last = datetime.datetime.now()
        try:
            if is_workday(april_last):  # 判断当前时间是不是节假日
                hours = int(april_last.strftime("%H"))
                if hours >= 9 and hours < 19:  # 判断当前时间是不是工作时间
                    isWorkTime = True
                    isWorkTime_mark = True
                    # print("现在是工作日的工作时间")
                    if hours >= 18 and request.session['user_name'] == "T4":
                        isWorkTime_mark = False
                else:
                    isWorkTime = False
                    isWorkTime_mark = False
                    # print("现在是工作日的非工作时间")
            else:
                isWorkTime = False
                isWorkTime_mark = False
                # print("现在是非工作日时间")
        except Exception as e:
            print(e)
            isWorkTime = True  # 当chinese_calendar日历库不能使用时，则把当前时间看作工作时间
            isWorkTime_mark = False  # 当chinese_calendar日历库不能使用时，同时看作非工作时间

    if request.method == 'POST':

        # 录入新系统，给新系统定义类型：第一类、第二类、第三类
        if request.POST.get('system_input') == 'system_input':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                systemType = request.POST.get('systemType')
                systemEnglishName = request.POST.get('systemEnglishName')
                systemChineseName = request.POST.get('systemChineseName')

                # 去空格，中文逗号转英文逗号
                systemChineseName = replaceName(systemChineseName)
                systemEnglishName = replaceName(systemEnglishName)

                systemName = systemEnglishName + '（' + systemChineseName + '）'

                # 添加内容
                if deploymentInfo.check_section(request.session['user_name']):
                    deploymentInfo.set_section(request.session['user_name'], systemName, systemType)
                    deploymentInfo.save()
                    message = '添加成功！'
                else:
                    deploymentInfo.add_section(request.session['user_name'])
                    deploymentInfo.set_section(request.session['user_name'], systemName, systemType)
                    deploymentInfo.save()
                    message = '添加成功！'

        # 删除系统
        if request.POST.get('system_delete') == 'system_delete':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                systemName = request.POST.get('systemName')
                try:
                    deploymentInfo.remove_key(request.session['user_name'], systemName)
                    deploymentInfo.save()
                    message = '删除成功！'
                except Exception as e:
                    print(e)
                    message = '删除失败！ 原因：%s' % e

        # 新增非窗口期部署申请记录
        if request.POST.get('deploy_input') == 'deploy_input':
            if isWorkTime:
                loginUser = request.session['user_name']
                systemName = request.POST.get('systemName')
                applicant = request.POST.get('applicant')
                applicantTime = request.POST.get('applicantTime')
                reasonType = request.POST.get('reasonType')
                reason = request.POST.get('reason')

                applicantTime = applicantTime.replace('T', ' ')
                applicantTime = applicantTime + ':00'
                modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                systemType = deploymentInfo.get_value(request.session['user_name'], systemName)

                addApplicantDeploymentInfo = ApplicantDeploymentInfo.applicantDeployment.create()
                addApplicantDeploymentInfo.loginUser = loginUser
                addApplicantDeploymentInfo.systemName = systemName
                addApplicantDeploymentInfo.systemType = systemType
                addApplicantDeploymentInfo.applicant = applicant
                addApplicantDeploymentInfo.applicantTime = applicantTime
                addApplicantDeploymentInfo.reasonType = reasonType
                addApplicantDeploymentInfo.reason = reason
                addApplicantDeploymentInfo.modifyTime = modifyTime
                addApplicantDeploymentInfo.save()
                message = '提交成功！'
            else:
                message = '提交失败，填写位置错误，请刷新页面重新提交！'

        # 测试/开发自行部署记录
        if request.POST.get('deploy_input2') == 'deploy_input2':
            if not isWorkTime_mark:
                loginUser = request.session['user_name']
                systemName = request.POST.get('systemName')
                deploymentPersonnel = request.POST.get('deploymentPersonnel')
                role = request.POST.get('role')
                deploymentTime = request.POST.get('deploymentTime')

                deploymentTime = deploymentTime.replace('T', ' ')
                deploymentTime = deploymentTime + ':00'
                modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                addSelfDeploymentInfo = SelfDeploymentInfo.selfDeployment.create()
                addSelfDeploymentInfo.loginUser = loginUser
                addSelfDeploymentInfo.systemName = systemName
                addSelfDeploymentInfo.deploymentPersonnel = deploymentPersonnel
                addSelfDeploymentInfo.role = role
                addSelfDeploymentInfo.deploymentTime = deploymentTime
                addSelfDeploymentInfo.modifyTime = modifyTime
                addSelfDeploymentInfo.save()
                message = '提交成功！'
            else:
                message = '提交失败，填写位置错误，请刷新页面重新提交！'

        # 删除非窗口期部署申请记录
        if request.POST.get('delete_system_input') == 'delete_system_input':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                applicantTime = request.POST.get('applicantTime')
                modifyTime = request.POST.get('modifyTime')

                try:
                    getApplicantDeploymentInfo_list = ApplicantDeploymentInfo.applicantDeployment.filter(
                        loginUser=loginUser, id=id, modifyTime=modifyTime)
                except Exception as e:
                    logging.info("ERROR：来自：%s, " % e)
                    getApplicantDeploymentInfo_list = None
                    message = "删除数据失败，获取不到对应的数据！"

                # 删除数据
                if getApplicantDeploymentInfo_list:
                    for applicantDeploymentInfo in getApplicantDeploymentInfo_list:
                        applicantDeploymentInfo.delete()
                        message = "删除数据成功！"

        # 删除测试/开发自行部署记录
        if request.POST.get('delete_system_input2') == 'delete_system_input2':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                modifyTime = request.POST.get('modifyTime')

                try:
                    getSelfDeploymentInfo_list = SelfDeploymentInfo.selfDeployment.filter(
                        loginUser=loginUser, id=id, modifyTime=modifyTime)
                except Exception as e:
                    logging.info("ERROR：来自：%s, " % e)
                    getSelfDeploymentInfo_list = None
                    message = "删除数据失败，获取不到对应的数据！"

                # 删除数据
                if getSelfDeploymentInfo_list:
                    for selfDeploymentInfo in getSelfDeploymentInfo_list:
                        selfDeploymentInfo.delete()
                        message = "删除数据成功！"

    # 获取用户下所有系统名称
    if deploymentInfo.check_section(request.session['user_name']):
        allSystemName = deploymentInfo.get_keys(request.session['user_name'])

    # 当前时间
    start_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    try:
        # 获取数据【非窗口期部署申请】
        getApplicantDeploymentInfo_list = ApplicantDeploymentInfo.applicantDeployment.filter(
            loginUser=request.session['user_name'], isDelete=False).order_by('-id')
    except Exception as e:
        print(e)
        getApplicantDeploymentInfo_list = None

    try:
        # 获取数据【测试/开发自行部署登记】
        getSelfDeploymentInfo_list = SelfDeploymentInfo.selfDeployment.filter(
            loginUser=request.session['user_name'], isDelete=False).order_by('-id')
    except Exception as e:
        print(e)
        getSelfDeploymentInfo_list = None

    return render(request, 'software/countDeploymentInfo.html', locals())


def myServerInfo(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))


    if not request.session.get('is_login', None):
        message = "您尚未登录，使用【服务器信息】请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == "POST":
        # print('------------------------')
        # print(request.POST.get('deleted'))
        # print(request.POST.get('create'))
        # print('------------------------')
        ###### 新增和删除测试环境数据库信息 starting ######
        if request.POST.get('operating') == 'deleted':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                modifyTime = request.POST.get('modifyTime')
                uatDataBase = UatDataBaseInfo.uatdatabase.filter(loginUser=loginUser, id=id, modifyTime=modifyTime)
                uatDataBase.delete()
                # print('%s删除成功！' % uatDataBase)
        elif request.POST.get('operating') == 'create':
            newUatDataBase = UatDataBaseInfo.uatdatabase.create()
            newUatDataBase.loginUser = request.session['user_name']
            newUatDataBase.blongTo = request.POST.get('blongTo').replace(" ", "")
            newUatDataBase.domain = request.POST.get('domain').replace(" ", "")
            newUatDataBase.dataBaseLink = request.POST.get('dataBaseLink').replace(" ", "")
            newUatDataBase.dataBaseName = request.POST.get('dataBaseName').replace(" ", "")
            newUatDataBase.userName = request.POST.get('userName').replace(" ", "")
            newUatDataBase.remark = request.POST.get('remark').replace(" ", "")
            newUatDataBase.envType = request.POST.get('envType').replace(" ", "")
            newUatDataBase.modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            newUatDataBase.save()
        ###### 新增和删除测试环境数据库信息 end  ##########

        ###### 新增和删除测试环境服务器信息 starting ######
        elif request.POST.get('operating') == 'addServer':
            ip = request.POST.get('ip').replace(" ", "")
            ip = ip.replace("，", ",")
            ip_list = ip.split(',')
            for ip in ip_list:
                addMyServerInfo = MyServerInfo.myServer.create()
                addMyServerInfo.loginUser = request.session['user_name']
                addMyServerInfo.blongTo = request.POST.get('blongTo').replace(" ", "")
                addMyServerInfo.domainName = request.POST.get('domainName').replace(" ", "")
                addMyServerInfo.envType = request.POST.get('envType').replace(" ", "")
                addMyServerInfo.appid = request.POST.get('appid').replace(" ", "")
                addMyServerInfo.ip = ip
                addMyServerInfo.applicantName = request.POST.get('applicantName').replace(" ", "")
                addMyServerInfo.applicantType = request.POST.get('applicantType').replace(" ", "")
                addMyServerInfo.deployPlatform = request.POST.get('deployPlatform').replace(" ", "")
                addMyServerInfo.remark = request.POST.get('remark').replace(" ", "")
                addMyServerInfo.modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                addMyServerInfo.save()
        elif request.POST.get('operating') == 'delServer':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                modifyTime = request.POST.get('modifyTime')
                delMyServer = MyServerInfo.myServer.filter(loginUser=loginUser, id=id, modifyTime=modifyTime)
                delMyServer.delete()
                # print('%s删除成功！' % delMyServer)
        ###### 新增和删除测试环境服务器信息 end ##########

        ###### 新增和删除gtilab代码库信息 starting ######
        elif request.POST.get('operating') == 'addGitlabInfo':
            # print(type(request.POST.getlist('packageType')))
            # print(request.POST.getlist('packageType'))
            # print('---------------------------------')
            # print(type(request.POST.get('packageType')))
            # print(request.POST.get('packageType'))

            addGitlab = MyGitlabInfo.myGitlab.create()
            addGitlab.loginUser = request.session['user_name']
            addGitlab.blongTo = request.POST.get('blongTo').replace(" ", "")
            addGitlab.packageName = request.POST.get('packageName').replace(" ", "")
            addGitlab.appid = request.POST.get('appid').replace(" ", "")
            addGitlab.gitlabBase = request.POST.get('gitlabBase').replace(" ", "")
            addGitlab.projectId = request.POST.get('projectId').replace(" ", "")
            addGitlab.wizardSpace = request.POST.get('wizardSpace').replace(" ", "")
            addGitlab.system = request.POST.get('system').replace(" ", "")
            addGitlab.person = request.POST.get('person').replace(" ", "")
            addGitlab.type = request.POST.get('packageType')
            addGitlab.remark = request.POST.get('remark').replace(" ", "")
            addGitlab.modifyTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            addGitlab.save()
        elif request.POST.get('operating') == 'delGitlab':
            if not request.session.get('manager_islogin', None):
                message = "您尚未登录超级用户，请先登录！！"
            else:
                loginUser = request.session['user_name']
                id = request.POST.get('id')
                modifyTime = request.POST.get('modifyTime')
                delMyGitlab = MyGitlabInfo.myGitlab.filter(loginUser=loginUser, id=id, modifyTime=modifyTime)
                delMyGitlab.delete()
                # print('%s删除成功！' % delMyGitlab)
        ###### 新增和删除gtilab代码库信息 end  ##########

    try:
        getMyServerInfo_list = MyServerInfo.myServer.filter(loginUser=request.session['user_name']).order_by('envType',
                                                                                                             'applicantType',
                                                                                                             'domainName',
                                                                                                             'appid',
                                                                                                             'applicantName')

        myServer_blongTo_list = []
        myServer_envType_list = []
        myServer_domain_list = []
        myServer_applicantType_list = []
        myServer_deployPlatform_list = []
        for myServer in getMyServerInfo_list:
            myServer_blongTo_list.append(myServer.blongTo)
            myServer_envType_list.append(myServer.envType)
            myServer_domain_list.append(myServer.domainName)
            myServer_applicantType_list.append(myServer.applicantType)
            myServer_deployPlatform_list.append(myServer.deployPlatform)
        myServer_blongTo_list = list(set(myServer_blongTo_list))
        myServer_envType_list = list(set(myServer_envType_list))
        myServer_domain_list = list(set(myServer_domain_list))
        myServer_applicantType_list = list(set(myServer_applicantType_list))
        myServer_deployPlatform_list = list(set(myServer_deployPlatform_list))

        allMyServer_blongTo_dict = {}
        for blongTo in myServer_blongTo_list:
            same_blongTo_list = []
            for myServer in getMyServerInfo_list:
                if myServer.blongTo == blongTo:
                    same_blongTo_list.append(myServer)
            allMyServer_blongTo_dict[blongTo] = same_blongTo_list
        # print('allMyServer_blongTo_dict: ', allMyServer_blongTo_dict)
    except Exception as e:
        print(e)
        getMyServerInfo_list = None

    try:
        getUatDataBaseInfo_list = UatDataBaseInfo.uatdatabase.filter(
            ~Q(envType='prd') & Q(loginUser=request.session['user_name'])).order_by('domain', 'envType')

        blongTo_list = []
        envType_list = []
        dataBaseDomain_list = []
        for uatDataBaseInfo in getUatDataBaseInfo_list:
            blongTo_list.append(uatDataBaseInfo.blongTo)
            envType_list.append(uatDataBaseInfo.envType)
            dataBaseDomain_list.append(uatDataBaseInfo.domain)
        blongTo_list = list(set(blongTo_list))
        envType_list = list(set(envType_list))
        dataBaseDomain_list = list(set(dataBaseDomain_list))

        all_blongTo_dict = {}
        for blongTo in blongTo_list:
            same_blongTo_list = []
            for uatDataBaseInfo in getUatDataBaseInfo_list:
                if uatDataBaseInfo.blongTo == blongTo:
                    same_blongTo_list.append(uatDataBaseInfo)
            all_blongTo_dict[blongTo] = same_blongTo_list
        # print('all_blongTo_dict: ', all_blongTo_dict)
    except Exception as e:
        print(e)
        getUatDataBaseInfo_list = None

    try:
        getMyGitlabInfo_list = MyGitlabInfo.myGitlab.filter(loginUser=request.session['user_name'],
                                                            isDelete=False).order_by('-id')

        blongTo_list = []
        wizardSpace_list = []
        for myGitlabInfo in getMyGitlabInfo_list:
            blongTo_list.append(myGitlabInfo.blongTo)
            wizardSpace_list.append(myGitlabInfo.wizardSpace)
        blongTo_list = list(set(blongTo_list))
        wizardSpace_list = list(set(wizardSpace_list))

        all_myGitlabInfo_blongTo_dict = {}
        for blongTo in blongTo_list:
            same_blongTo_list = []
            for myGitlabInfo in getMyGitlabInfo_list:
                if myGitlabInfo.blongTo == blongTo:
                    same_blongTo_list.append(myGitlabInfo)
            all_myGitlabInfo_blongTo_dict[blongTo] = same_blongTo_list
        # print('all_myGitlabInfo_blongTo_dict: ', all_myGitlabInfo_blongTo_dict)
    except Exception as e:
        print(e)
        getMyGitlabInfo_list = None

    return render(request, 'software/myServerInfo.html', locals())


def test(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))

    path = 'config/software_config/report_check_list_config2.ini'
    try:
        config_1 = getConfig(path)
        print('-----------------------------------------------------------------1')
        print(config_1.get_items('report_check_list'))
        print('-----------------------------------------------------------------2')
        print(config_1.check_section('report_check_list'))
        print('-----------------------------------------------------------------3')
        print(config_1.check_key('report_check_list', 'ALL'))
        print('-----------------------------------------------------------------4')
        print(config_1.check_value('report_check_list', 'ALL', '发布检查单qwe'))
        print('-----------------------------------------------------------------5')
        print(config_1.add_section('user'))
        print('-----------------------------------------------------------------6')
        print(config_1.set_section('user', 'b', '2'))
        print(config_1.set_section('user', 'c', '4'))
        print('-----------------------------------------------------------------7')
        print(config_1.remove_key('user', 'b'))
        print(config_1.save())
        print('-----------------------------------------------------------------8')
        # print(config_1.clear())
        print('-----------------------------------------------------------------9')
        print('-----------------------------------------------------------------10')
        print('-----------------------------------------------------------------11')
        print('-----------------------------------------------------------------12')
        print('-----------------------------------------------------------------13')
        print('-----------------------------------------------------------------14')
        print('-----------------------------------------------------------------15')
    except:
        print('路径有问题！')
    return render(request, 'test.html', locals())
