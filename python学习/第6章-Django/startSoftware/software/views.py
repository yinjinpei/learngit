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
import ast
import logging
import configparser
import shutil

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

# 启动异步定时任务
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_job

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


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

# 实例化调度器
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
# 调度器开始
scheduler.start()


# print('-'*100)
# print('所有定时任务：',scheduler.get_jobs())
# print('-'*100)

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
    def get_keys(self,section):
        return self.config.options(section)
    # 获取指定 key 的 value,以字符串形式串返回
    def get_value(self,section,key):
        return self.config.get(section,key)
    # 获取指定 key 的 value(value必须是整数类型),返回为int类型
    def getint_value(self,section,key):
        return self.config.getint(section,key)
    # 获取指定 key 的 value(value必须是浮点数类型),返回为float类型
    def getfloat_value(self,section,key):
        return self.config.getfloat(section,key)
    # 获取指定 key 的 value(value必须是布尔数类型),返回为boolean类型
    def getboolean_value(self,section,key):
        return self.config.getboolean(section,key)
    # 获取指定 section 的 keys & values
    def get_items(self,section):
        return self.config.items(section)  # 注意items()返回的字符串会全变成小写

    # 检查section（节点）是否存在
    def check_section(self,section):
        return section in self.config
    # 检查section（节点）下的key 是否存在
    def check_key(self,section,key):
        return key in self.config[section]
        # 检查section（节点）下的key的value值是否包含self.value，类似字符串匹配
    def check_value(self,section,key,value):
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


def logoutSuperManager(request):
    del request.session['manager_islogin']
    return render(request, 'software/index.html')


# 检查是否登录超级管理用户
def loginSuperManager(request):
    manager = ManagerForm()
    setpassword = SetPasswordForm()

    if request.session.get('manager_islogin', None):
        print('manager_islogin值：',request.session.get('manager_islogin', None))
        manager_islogin = True
    else:
        # 如果用户的二级密码在数据库中有数据了就不是首次登录
        print('如果用户的二级密码在数据库中有数据了就不是首次登录')
        try:
            managers = ManagerDate.managers.get(user=request.session['user_name'])
            print('不是首次登录！')
            message = '请输入二级密码！'
            first_login = False
        except:
            message='首次登录，请设置二级密码！'
            print('是首次登录！')
            first_login = True

        # 要求用户输入二级密码并处理，保存至cokie
        if request.method == "POST":
            print('要求用户输入二级密码并处理，保存至cokie')
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
                # 如果提示某字段不能为空，请到数据库手工修改可以为空值，即把：不是null 的勾去掉
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


def up_one_level(dirname):
    print('上一层,dirname的值：',dirname)
    if dirname[-1] == '/':
        dirname = dirname[:-1]
    # 上一层目录完整路径
    up_one_level_path_tmp = ''
    result = dirname.split('/')
    for i in range(len(result) - 1):
        up_one_level_path_tmp += result[i] + '/'

    print('上一层目录为：',up_one_level_path_tmp[:-1])
    return up_one_level_path_tmp[:-1]

def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if dir_list:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
    # print('dir_list:',dir_list)
    return dir_list

def downloadFileInfo(path):
    fileObjectList = [] # 存放文件对象
    dirObjectList = []  # 存放目录对象

    fileList = os.listdir(path)

    # 获取的文件或目录按照最后修改时间顺序升序排列
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
            print('【%s】:这是一个文件' % file)
        elif os.path.isdir(path + file):
            print('【%s】：这是一个目录' % file)
            dirObject=AbsolutePath(file, path + file)
            dirObjectList.append(dirObject)
        else:
            print('path:',path)
            print('file',file)
            print('未知文件，无法识别该文件！！')

    for file in fileList2:
        if os.path.isfile(path + file):
            print('【%s】:这是一个文件' % file)
            filepath = path + file
            print('文件完整路径：【%s】' % filepath)

            fileSize = os.path.getsize(filepath)  # 获取文件大小
            fileSize = fileSize / float(1024)
            fileSize = round(fileSize, 2)

            fileCreatTime = os.path.getmtime(filepath)  # 获取文件修改时间
            fileCreatTime = datetime.datetime.fromtimestamp(fileCreatTime)
            fileCreatTime = fileCreatTime.strftime('%Y-%m-%d %X')

            fileObject = DownloadFileObject(file, fileSize, fileCreatTime, path)  # 创建文件对象
            fileObjectList.append(fileObject)  # 把文件对象存放到列表

        elif os.path.isdir(path + file):
            print('【%s】：这是一个目录' % file)
        else:
            print('path:',path)
            print('file',file)
            print('未知文件，无法识别该文件！！')


    return fileObjectList,dirObjectList


#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_dir,output_filename):
  zipf = zipfile.ZipFile(output_dir+'/'+output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()

def zipDir(sourcePath, outFullName, password=None):
    """
    压缩指定文件夹
    :param sourcePath: 目标文件夹路径
    :param outFullName: 保存路径+xxxx.zip
    :return:
    """

    print('sourcePath: ',sourcePath)
    print('sourcePath: ',outFullName)
    print('password: ',password)

    if password:
        cmd = "zip -P %s -r %s %s" % (password, outFullName, sourcePath)   #有密码时设置密码并压缩
    else:
        cmd = "zip -r %s %s" % (outFullName, sourcePath)   #无密码直接压缩
    try:
        # 执行系统命令
        os.popen(cmd)
        return True
    except Exception as e:
        print(e)
        return False


def match_productionMaterials(user_name,domain_name,file_path):
    '''
    :param user_name: 登录用户名
    :param domain_name: 领域名
    :param file_path: 文件的完整路径
    :return: 返回字典
    '''

    # 获取版本号
    version=file_path.split('/')[-1].split('（')[0]
    if version is None:
        version=domain_name

    # 获取所有文件名
    file_list = os.listdir(file_path)
    if len(file_list) == 0:
        return False

    report_config = configparser.ConfigParser()
    report_config.read('config\\software_config\\report_check_list_config.ini', encoding='UTF-8')

    # 获取领域所需要检查的报告
    check_report = report_config.get('report_check_list', domain_name)
    if len(check_report) == 0:
        return False
    # 去空格
    check_report=check_report.strip()
    # 把字符串(配置)转换为列表
    check_report=check_report.split(',')

    print('---------------------------------------------------')
    print('%s检查报告列表：%s' % (domain_name, check_report))
    print('---------------------------------------------------')

    # 获取所有检查报告，不分前后端
    all_check_report=report_config.get('report_check_list', 'all')
    # 去空格
    all_check_report = all_check_report.strip()
    # 把字符串(配置)转换为列表
    all_check_report = all_check_report.split(',')

    all_check_report.insert(0,'版本号')

    # 初始化，把所有检查的报告都初始化为X，类型为字典，key为报告类型名、value为X
    all_check_report_dict = {}
    for report in all_check_report:
        all_check_report_dict[report]='X'

    for report in all_check_report:
        try:
            findStr = report_config.get('match_keywords',report)
            # print('%s 的匹配关键字：'%report,findStr)
        except Exception as e:
            print(e)
            print('本次匹配没有匹配到对应的报告类型！')
            continue

        for file in file_list:
            matchStr = re.findall(findStr, str(file), re.M | re.I | re.S)
            if matchStr:
                print('【%s】:【%s】 报告已上传！！' % (report,file))
                all_check_report_dict[report] = '✔'
                print(all_check_report_dict)
                break


    # 筛选出不涉及的相关测试报告
    uncheck_report = list(set(all_check_report).difference(check_report))
    for report in uncheck_report:
        all_check_report_dict[report] = '不涉及'
    print('uncheck_report 数据类型：', type(uncheck_report))
    print('不涉及的相关测试报告：', uncheck_report)

    all_check_report_dict['版本号']=version
    print('%s 领域收集投产材料情况：%s'%(version, all_check_report_dict))

    return all_check_report_dict


def delFile(request):
    user_management_config = getConfig('config\\software_config\\user_management_config.ini')
    # 黑名单目录下不显示上传功能
    versionManagerUsers = user_management_config.get_value('user_list', 'black_user_list').split(',')
    print('删除文件')

    user_home = 'uploads/' + request.session['user_name'] + '/'
    if request.session['user_name'] in versionManagerUsers:
        print('登录的用户名是：', request.session['user_name'])
        shar_dir_list = []  # shar用户家目录的文件夹列表

        for user in versionManagerUsers:
            shar_dir_list.append('uploads/' + user + '/')

        for dir in os.listdir(user_home):
            if os.path.isdir(user_home + dir):
                shar_dir_list.append(user_home + dir + '/')
        print('不在这些目录下展示上传功能：', shar_dir_list)

    if request.method == "POST":
        user_home = 'uploads/' + request.session['user_name'] + '/'
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        print('删除文件使用POST方式')

        dirname = request.GET.get('dirname')
        if dirname:
            print('dirname确实存在！！！！！！！！',dirname)
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
        print('~~~~~~~~~~~~~~~dirname：', dirname)

        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'

        downloadFileName = request.POST.get('downloadFileName')
        print('===================----------------=======================')
        print(downloadFileName)
        print('===================----------------=======================')

        if downloadFileName is not None:
            lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
            if lockbaseinfo:
                islock = lockbaseinfo[0].islock
                if islock:
                    del_file_message = '已锁库，禁止上传和删除！'
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
                print('dirname不是空值：',dirname)

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
                path=dirname+'/'

        deleted_dir_name = request.POST.get('deleted_dir_name')
        print('===================----------------=======================')
        print(deleted_dir_name)
        print('===================----------------=======================')
        if deleted_dir_name is not None:
            if os.path.exists(path+deleted_dir_name):
                shutil.rmtree(path=path+deleted_dir_name)

            if dirname != 'None':
                print('dirname不是空值：',dirname)

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
                path=dirname+'/'

        delFile_form = DelFile(request.POST)
        if delFile_form.is_valid(): # 如果有数据
            print('有删除数据提交！！！')
            dirname = request.POST.get('dirname')
            print('dirname  POST方式的值是',dirname)
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
                    del_file_message = '已锁库，禁止上传和删除！'
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
        print('~~~~~~~~~~~~~~~dirname：', dirname)

        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        fileObjectList, dirObjectList = downloadFileInfo(path)

        delFile_form = DelFile()
        return render(request, 'software/uploadFile.html', locals())

def uploadFile(request):
    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【文件管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    path = 'uploads/' + request.session['user_name'] + '/'  # 上传文件路径，相对路径，在项目根目录下
    if not os.path.exists(path):  # 目录不存在则创建
        os.makedirs(path)

    user_management_config = getConfig('config\\software_config\\user_management_config.ini')
    # 版本管理用户,黑名单目录下不显示上传功能
    versionManagerUsers = user_management_config.get_value('user_list', 'black_user_list').split(',')

    # 用户家目录
    user_home ='uploads/' + request.session['user_name'] + '/'
    if request.session['user_name'] in versionManagerUsers:
        print('登录的用户名是：', request.session['user_name'])
        shar_dir_list = []  # shar用户家目录的文件夹列表

        for user in versionManagerUsers:
            shar_dir_list.append('uploads/' + user + '/')

        for dir in os.listdir(user_home):
            if os.path.isdir(user_home + dir):
                shar_dir_list.append(user_home + dir + '/')
        print('不在这些目录下展示上传功能：', shar_dir_list)

    delFile_form = DelFile()  # 宣染删除表格，即宣染删除功能的输入框

    dirname = request.GET.get('dirname')

    if dirname is not None:
        userRootPath = dirname.split('/')[1]
        print('当前获取的用户家目录：', userRootPath)
        if request.session['user_name'] != userRootPath:
            return render(request, 'software/ERROR.html')

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
            print('=' * 50 + '获取到的绝对路径path：', path)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'
        else:
            print('*' * 50 + '获取到的绝对路径：', dirname)
            return HttpResponse('<h4 style="color: red;font-weight: bold">访问错误,访问网页不存在！</h4>')
    else:
        dirname=path[:-1]

    fileObjectList, dirObjectList = downloadFileInfo(path)

    if request.method == 'POST':
        dirname = request.POST.get('dirname')
        print('--------------------------获取到的目录-----------------------------')
        print(dirname)
        print('------------------------------------------------------------------')

        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]
            up_one_level_path = up_one_level(dirname)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'

            path=dirname+'/'
            print('----------------------------当前路径-------------------------------')
            print(path)
            print('------------------------------------------------------------------')

        # file = request.FILES['file']  # 获取单个上传的文件对象，如果上传了多个，只取最后一个
        uploadFileList=request.FILES.getlist('file') # 获取所有上传的文件对象
        print('************************所有上传的文件对象**************************')
        print(uploadFileList)
        print('******************************************************************')

        islock_base = request.POST.get('lock_base')  # 获取所有上传的文件对象
        print('************************是否被锁库**************************')
        print(islock_base)
        print('******************************************************************')

        if islock_base:
            print('islock_base')
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
            print(message)

        repeatFileList = [] # 记录重名的文件名
        upload_list_successful=[] # 记录上传成功的文件名
        repeatFileSum=0 # 重名文件的总个数

        lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
        if lockbaseinfo:
            islock = lockbaseinfo[0].islock
            if islock:
                message='已锁库，禁止上传和删除！'
            else:
                if uploadFileList:
                    for file in uploadFileList:
                        print(len(uploadFileList))
                        fileName=str(file) # 上传的文件名
                        print("================== 文件名%s============="%fileName)
                        print(path+fileName)

                        if os.path.exists(path+fileName):
                            repeatFileList.append(fileName) # 记录重名的文件名
                            continue
                            # return render(request, 'software/uploadFile.html', locals())
                        with open(path + fileName, 'wb+') as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)
                        upload_list_successful.append(fileName) # 记录成功上传的文件名

                    message="%d个文件上传成功，%d个文件上传失败！！"%(len(upload_list_successful),len(repeatFileList))
                    if len(upload_list_successful) !=0:
                        upload_successful_message="上传成功列表：%s"%upload_list_successful
                    if len(repeatFileList) != 0:
                        upload_failure_message = "【%d个文件重名，请重新命名再上传！】 失败列表:%s"%(len(repeatFileList),repeatFileList)
        else:
            if uploadFileList:
                for file in uploadFileList:
                    print(len(uploadFileList))
                    fileName = str(file)  # 上传的文件名
                    print("================== 文件名%s=============" % fileName)
                    print(path + fileName)

                    if os.path.exists(path + fileName):
                        repeatFileList.append(fileName)  # 记录重名的文件名
                        continue
                        # return render(request, 'software/uploadFile.html', locals())
                    with open(path + fileName, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    upload_list_successful.append(fileName)  # 记录成功上传的文件名

                message = "%d个文件上传成功，%d个文件上传失败！！" % (len(upload_list_successful), len(repeatFileList))
                if len(upload_list_successful) != 0:
                    upload_successful_message = "上传成功列表：%s" % upload_list_successful
                if len(repeatFileList) != 0:
                    upload_failure_message = "【%d个文件重名，请重新命名再上传！】 失败列表:%s" % (len(repeatFileList), repeatFileList)
    else:
        message='温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        print(message)

    lockbaseinfo = LockBaseInfo.lockbase.filter(pathName=dirname)
    if lockbaseinfo:
        islock = lockbaseinfo[0].islock
        print('islock', islock)
    else:
        islock = False
    fileObjectList, dirObjectList = downloadFileInfo(path)

    return render(request, 'software/uploadFile.html', locals())



def downloadFile(request,fileObject=None):
    if fileObject is None:
        # 获取上传文件路径和文件名，用于单个文件下载
        fileObject = request.POST.get('name')
        # 提取文件名
        tmp_list =fileObject.split('/')
        filename = tmp_list[-1]
    else:
        tmp_list = fileObject.split('/')
        filename = tmp_list[-1].split('_')[-1]
    # file = open(path+filename,'rb')
    print('000000000000000000000000000000000')
    print('文件名：',filename)
    print('完整的路径：',fileObject)
    print('000000000000000000000000000000000')
    try:
        file = open(fileObject,'rb')
    except:
        return HttpResponse('下载文件名有错，请联系管理员！  文件名：%s'%fileObject)
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
    dirname = request.GET.get('dirname')
    path=dirname
    print('dirname GET方式传递过来的值:',dirname)
    up_one_level_path=up_one_level(path)
    print('up_one_level_path：',up_one_level_path)


    # 获取领域名
    domainName = dirname.split('/')[2]
    domainName = domainName.split('（')[0]

    config=getConfig('config\\software_config\\user_management_config.ini')
    user_list=config.get_value('user_list','black_user_list')
    user_list2=user_list.split(',')

    # 如果是创建版本号目录则按版本目录规则创建目录
    if request.session['user_name'] in user_list2:
        print(request.session['user_name'])
        if up_one_level_path=='uploads':
            if not request.session.get('manager_islogin', None):
                message = "创建一级目录需要超级用户权限，您尚未登录超级用户，请先登录！！"
                return render(request, 'software/ERROR.html',locals())

        if path != 'uploads/' + request.session['user_name'] + '/1-版本检查单（收集）/':
            limit = True
            print('limit：',limit)

        # 新增领域文件目录时，使用领域命名格式如:BCES-SECU（网银安全子系统）
        if path == 'uploads/' + request.session['user_name']+'/':
            domain_naming=True
            print('domain_naming：', domain_naming)

        for username in user_list2:
            if up_one_level_path == 'uploads/'+username:
                black_user=True
                print('black_user：', black_user)
                break

    if request.method == "POST":
        dirname = request.POST.get('dirname')
        print('dirname POST方式传递过来的值:', dirname)

        # 创建领域目录
        createDirectory_from = CreateDirectory(request.POST)
        if createDirectory_from.is_valid():
            engilistName=createDirectory_from.cleaned_data['englishName']
            chineseName=createDirectory_from.cleaned_data['chineseName']
            try:
                os.makedirs(dirname+engilistName+'（'+chineseName+'）')
                message="%s 创建目录成功！"%(engilistName+'（'+chineseName+'）')
            except:
                message = "%s 创建目录失败，请检查目录是否已存在！" % (engilistName+'（'+chineseName+'）')
            print(message)


        # 创建普通目录
        newDirectory_form = NewDirectory(request.POST)
        if newDirectory_form.is_valid():  # 如果有数据
            DirectoryName = newDirectory_form.cleaned_data['DirectoryName'] # 获取新建文件夹名
            try:
                os.makedirs(dirname+DirectoryName)
                message="%s 创建目录成功！"%(DirectoryName)
            except:
                message = "%s 创建目录失败，请检查目录是否已存在！" % (DirectoryName)
            print(message)

        # 创建版本目录
        CreateVersionDirectory_form=CreateVersionDirectory(request.POST)
        if CreateVersionDirectory_form.is_valid():  # 如果有数据
            VersionName = CreateVersionDirectory_form.cleaned_data['VersionName']  # 获取新建文件夹名,版本号
            Date = str(CreateVersionDirectory_form.cleaned_data['Date'])  # 获取投产日期

            name = VersionName[:len(domainName)]
            number=VersionName[len(domainName):]
            try:
                number_1,number_2,number_3 = number.split('.')
                print('number_1,number_2,number_3: ',number_1,number_2,number_3)

                #如果以下能转换成功说明全是数字，如果不能则报错
                number_1=int(number_1)
                number_2=int(number_2)
                number_3=int(number_3)

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
            print(message)

    createDirectory_from=CreateDirectory()
    newDirectory_form=NewDirectory()
    CreateVersionDirectory_form=CreateVersionDirectory()
    return render(request, 'software/newDirectory.html', locals())


def rename_directory(request):
    if not request.session.get('manager_islogin', None):
        uploadFile_message = "您尚未登录超级用户，请先登录！！"
        return render(request, 'software/index.html', locals())

    # 获取当前函数名
    function_name=sys._getframe().f_code.co_name

    dirname = request.GET.get('dirname')
    path=dirname
    print('dirname GET方式传递过来的值:',dirname)
    up_one_level_path=up_one_level(path)
    up_two_level_path = up_one_level(up_one_level_path)

    if dirname:
        if dirname[-1] == '/':
            dirname = dirname[:-1]

    old_dir_name=dirname.split('/')[-1]
    print('旧目录名：',old_dir_name)
    print('上一级目录名：',up_one_level_path)
    print('上二级目录名：',up_two_level_path)


    # 获取领域名
    domainName = dirname.split('/')[2]
    domainName = domainName.split('（')[0]

    config=getConfig('config\\software_config\\user_management_config.ini')
    user_list=config.get_value('user_list','black_user_list')
    user_list2=user_list.split(',')

    # 如果是创建版本号目录则按版本目录规则创建目录
    if request.session['user_name'] in user_list2:
        print(request.session['user_name'])
        if up_one_level_path != 'uploads/' + request.session['user_name'] + '/1-版本检查单（收集）':
            limit = True

        if up_one_level_path == 'uploads/' + request.session['user_name']:
            domain_naming=True
            print('domain_naming：', domain_naming)

        for username in user_list2:
            if up_two_level_path == 'uploads/'+username:
                black_user=True
                break

    if request.method == "POST":
        dirname = request.POST.get('dirname')
        print('dirname POST方式传递过来的值:', dirname)

        createDirectory_from = CreateDirectory(request.POST)
        if createDirectory_from.is_valid():
            engilistName = createDirectory_from.cleaned_data['englishName']
            chineseName = createDirectory_from.cleaned_data['chineseName']
            try:
                os.rename(up_one_level_path + '/' + old_dir_name, up_one_level_path + '/' + engilistName + '（' + chineseName + '）')
                message = "%s 修改目录成功！" % (engilistName + '（' + chineseName + '）')
            except:
                message = "%s 修改目录失败，请检查目录是否已存在！" % (engilistName + '（' + chineseName + '）')
            print(message)

        newDirectory_form = NewDirectory(request.POST)
        if newDirectory_form.is_valid():  # 如果有数据
            DirectoryName = newDirectory_form.cleaned_data['DirectoryName'] # 获取新建文件夹名
            print('获取新的目录名：',DirectoryName)
            print('旧的完整名：',up_one_level_path+'/'+old_dir_name)
            print('新的完整名：',up_one_level_path+'/'+DirectoryName)
            try:
                os.rename(up_one_level_path+'/'+old_dir_name,up_one_level_path+'/'+DirectoryName)
                message="%s 修改目录成功！"%(DirectoryName)
            except:
                message = "%s 修改目录失败，请检查目录是否已存在！" % (DirectoryName)
            print(message)

        CreateVersionDirectory_form=CreateVersionDirectory(request.POST)
        if CreateVersionDirectory_form.is_valid():  # 如果有数据
            VersionName = CreateVersionDirectory_form.cleaned_data['VersionName']  # 获取新建文件夹名,版本号
            Date = str(CreateVersionDirectory_form.cleaned_data['Date'])  # 获取投产日期

            name = VersionName[:len(domainName)]
            number=VersionName[len(domainName):]
            try:
                number_1,number_2,number_3 = number.split('.')
                print('number_1,number_2,number_3: ',number_1,number_2,number_3)

                #如果以下能转换成功说明全是数字，如果不能则报错
                number_1=int(number_1)
                number_2=int(number_2)
                number_3=int(number_3)

                new_name = VersionName + '（' + Date + '）'
                new_name = new_name.replace(" ", "")

                if name == domainName:
                    try:
                        os.rename(up_one_level_path+'/'+old_dir_name,up_one_level_path+'/'+new_name)
                        message = "%s 修改成功！" % (new_name)
                    except:
                        message = "%s 修改失败，请检查目录是否已存在！" % (new_name)
                else:
                    message = "%s 修改失败，目录格式错误！！" % (new_name)
            except:
                message = "%s 修改失败，目录格式错误！！" % (VersionName + '（' + Date + '）')
            print(message)

    createDirectory_from=CreateDirectory()
    newDirectory_form=NewDirectory()
    CreateVersionDirectory_form=CreateVersionDirectory()
    return render(request, 'software/rename_directory.html', locals())


def mycopy(src_file, dst_file):
    """此函数的功以实现复制文件
    src_file : 源文件名
    dst_file : 目标文件名
    """
    try:
        with open(src_file, "rb") as fr,open(dst_file, 'wb') as fw:
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
    # 获取文件原路径
    source_dir = request.GET.get('source_dir')
    print('source_dir GET方式传递过来的值:', source_dir)
    if source_dir[-1] == '/':
        source_dir = source_dir[:-1]
    # 生成临时目录作为打zip包目录，用户下载完成后会自动删除
    output_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")+'_'+source_dir.split('/')[-1]+'.zip'
    print('目录作为打zip包名：', output_filename)
    output_dir = 'uploads/'+ 'temp'
    print('存放zip包临时目录：', output_dir)
    # 临时目录不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 打包zip包
    make_zip(source_dir, output_dir, output_filename)
    print('打包完成！！！')
    return downloadFile(request,output_dir+'/'+output_filename)


def versionManagerIndex(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request,'software/versionManagerIndex.html')

def T8_index(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request,'software/T8_index.html')

def CDNofflink(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request,'software/CDNofflink.html')

def tdc(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request,'software/tdc.html')

def extranetAddress(request):
    clientIP = request.META['REMOTE_ADDR']
    webName = str(versionManagerIndex.__name__)
    logging.info(("INFO：来自：%s, 访问software/%s.html页面！！！") % (clientIP, webName))
    return render(request,'software/extranetAddress.html')


def setServerDate(request):
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
            ServerIP = date_form.cleaned_data['ServerIP']    # 获取IP
            MyJobID = request.session['user_name']+'_'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
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
            newTimer.setTime=ServerDatetime
            print('添加服务器IP----------------------------')
            newTimer.serverIP=ServerIP
            print('添加线程my_job_id----------------------------')
            newTimer.clientJobID=MyJobID
            print('保存到数据库----------------------------')
            newTimer.save()

            # 设置服务器时间
            def timerHelper(MyJobID):
                __username='root'
                __password='123456'
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
                        cmds=['export LANG=zh_CN.UTF-8','echo $LANG','pwd','ls -lh','hostname -i','date']
                        cmds.insert(0,set_time)

                        try:
                            print('创建SSH对象--------')
                            # 创建SSH对象
                            sf = paramiko.SSHClient()
                            # 允许连接不在know_hosts文件中的主机
                            sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            print('开始连接堡垒机服务器：%s'%self.serverIP)
                            # 连接服务器
                            sf.connect(hostname=self.serverIP, port=self.port, username=self.username,
                                       password=self.password)
                            print('连接堡垒机服务器成功！')

                            print('激活连接的终端！')
                            channel = sf.invoke_shell()
                            print('设置读、写操作超时时间')
                            channel.settimeout(10)
                            print('发送命令行：%s'%cmds)
                            time.sleep(0.5)

                            for command in cmds:
                                channel.send(command + '\n')
                                time.sleep(0.5)
                                try:
                                    command_res = channel.recv(65533).decode('utf-8')
                                    print('-' * 30)
                                    print(command_res)
                                    print('-' * 30)
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
                        jobisDelete=timer.isDelete
                        serverIP=timer.serverIP
                        setTime=timer.setTime.strftime("%Y-%m-%d %H:%M:%S") # 获取日期 如：2020-3-23 12:11:00
                        print(clientJobID,jobisDelete)

                        # 判断任务是否被删除了
                        if jobisDelete == 0:
                            # 执行任务
                            serverHelper=TheServerHelper(serverIP, __username, __password, setTime, port=22)
                            serverHelper.ssh_connectionServer()
                            timerInfo = TimingData.timers.get(clientJobID=MyJobID)
                            timerInfo.delete()
                        break

            def createTimedTasks(MyJobID,year,month,day,hour,minute,second):
                from apscheduler.schedulers.background import BackgroundScheduler
                sched = BackgroundScheduler()
                # cron定时调度（某一定时时刻执行），表示2017年3月22日17时19分07秒执行该程序
                sched.add_job(timerHelper, 'cron',id=MyJobID,
                              year=year, month=month, day=day, hour=hour, minute=minute, second=second,args=[MyJobID])

                # interval间隔调度，4个参数分别为：函数、类型、线程id、执行时间间隔
                # sched.add_job(job, 'interval', id=job_id, seconds=1)

                # date 定时调度（作业只会执行一次）
                # The job will be executed on November 6th, 2009 at 16:30:05
                # sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
                sched.start()
            message = '添加定时任务成功！！'

            exec_year=Datetime.strftime('%Y')
            exec_month=Datetime.strftime('%m')
            exec_day=Datetime.strftime('%d')
            exec_hour=Datetime.strftime('%H')
            exec_minute=Datetime.strftime('%M')
            exec_second=Datetime.strftime('%S')
            createTimedTasks(MyJobID,exec_year,exec_month,exec_day,exec_hour,exec_minute,exec_second)

    timersList = TimingData.timers.all()
    date_form=DateForm()
    deldate_form=DelForm()
    return render(request, 'software/setServerDate.html', locals())


def delServerDate(request):
    if request.method == "POST":
        try:
            clientJobID=request.POST.get('clientJobID')
            print(clientJobID)
            if clientJobID is not None:
                timerInfo = TimingData.timers.get(clientJobID=clientJobID)
                print(timerInfo)
                timerInfo.delete()
                successful_message="【%s】删除成功！！"%clientJobID
            else:
                deldate_form = DelForm(request.POST)  # DateForm 为models里对应的类名,作为date_form.is_valid()铺垫
                if deldate_form.is_valid():  # 如果有数据，models里对应的类名,类里面有几个变量就获取几个，如果有一个报错则为空
                    MyJobID = deldate_form.cleaned_data['MyJobID']  # 获取线程ID
                    failure_msg="【%s】删除失败！！"%MyJobID
                    timerInfo = TimingData.timers.get(clientJobID=MyJobID)
                    if MyJobID==timerInfo:
                        timerInfo.delete()
                        successful_message="【%s】删除成功！！"%MyJobID
                        print(successful_message)
        except:
            pass
    message = '添加定时任务'
    timersList = TimingData.timers.all()
    date_form = DateForm()
    deldate_form = DelForm()
    return render(request, 'software/setServerDate.html', locals())


def productionMaterials(request):
    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【投产材料管理】请先登录！！"
        return render(request, 'software/index.html', locals())

    user_management_config = getConfig('config\\software_config\\user_management_config.ini')
    # 访问此功能的白名单用户, 白名单可访问投产材料管理页面
    allow_users=user_management_config.get_value('user_list', 'allow_users_list').split(',')

    user_dir_list=[]
    if request.session['user_name'] in allow_users:
        user_path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        for dir in os.listdir(user_path):
            print(dir)
            print(user_path+dir)
            if os.path.isdir(user_path+dir):
                user_dir_list.append(dir)
        user_dir_list=sorted(user_dir_list)
        print('用户下所有目录名：',user_dir_list) #['BCOS-MNGT', 'BRON', 'BRON-CLSS', 'BRON-CRMP', 'BRON-LPSS']

        if request.method == "GET":
            dirname=request.GET.get('domain')
            print('GET方式获取到的dirname：',dirname)

            if dirname:
                version_dir_list=[]
                version_path = 'uploads/' + request.session['user_name'] + '/' + dirname +'/'
                print('当前路径：',version_path)
                for dir in os.listdir(version_path):
                    print('当前目录：',dir)
                    if os.path.isdir(version_path+dir):
                        version_dir_list.append(dir)
                version_dir_list=sorted(version_dir_list)
                print('当前所有版本：',version_dir_list)
        if request.method == "POST":
            # 获取目录，如：BCOS-MNGT（渠道作业管理系统）/BCOS-MNGT1.1.0（2020-05-10）
            version_name=request.POST.get('version_name')
            print('获取目录version_name：',version_name)
            # 获取领域名
            domain_name = version_name.split('/')[0]
            print('获取领域名domain_name：',domain_name)
            temp_domain_name=domain_name.split('（')[0]
            print('temp_domain_name：',temp_domain_name)
            # 获取完整路径，如：uploads/shar/BCOS-MNGT（渠道作业管理系统）/BCOS-MNGT1.1.0（2020-05-10）
            file_path = user_path+version_name
            print('获取完整路径file_path：',file_path)
            # 获取文件目录名,如：BCOS-MNT1.1.0（2020-05-14）
            domain_path=version_name.split('/')[1]
            print('获取文件目录名domain_path：',domain_path)
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
            print('-------------------test1---------------------------')
            print("当前目录名domain_name：", domain_name)
            print("领域名temp_domain_name：", temp_domain_name)
            print("文件路径file_path：",file_path)
            print('-------------------test1---------------------------')

            try:
                one_check_report_dict=match_productionMaterials(request.session['user_name'],temp_domain_name,file_path)
                print('查询的领域收集投产材料情况：', one_check_report_dict)
            except:
                print('查询单个领域收集投产材料情况失败，配置中没有对应领域数据！')

        # 投产日期集合
        date_list=[]
        # 获取前端传过来的日期，只查询筛选的日期版本
        checkoutDate=request.GET.get('checkoutDate')
        print('checkoutDate',checkoutDate)

        # 存放所有领域版本投产资料收集情况
        all_check_report_list=[]
        # 遍历用户下面所有领域，并检查投产材料收集情况
        for domain in user_dir_list:
            temp_domain_name=domain.split('（')[0]
            print('temp_domain_name: ',temp_domain_name)
            for dir in os.listdir(user_path+domain): # 获取用户下所有领域目录和文件
                print('dir: ',dir)
                # 获取所有投产日期
                try:
                    temp_date=dir.split('（')[1]
                    temp_date=temp_date.split('）')[0]
                    if temp_date not in date_list:
                        date_list.append(temp_date) # 给到前端显示

                    # 只查询筛选的日期版本
                    if checkoutDate:
                        if checkoutDate in dir:
                            print('只查询筛选的日期版本checkoutDate:%s, temp_date:%s, dir:%s'%(checkoutDate,temp_date,dir))
                        else:
                            print('checkoutDate: ',checkoutDate)
                            continue
                except:
                    print('目录格式不对！！')
                    # 只查询筛选的日期版本
                    if checkoutDate:
                        print('只查询筛选的日期版本')
                        print('checkoutDate: ',checkoutDate)
                finally:
                    print('date_list: ',date_list)

                print('=======================*********************++++++++++++++++++++++++++++')
                if os.path.isdir(user_path + domain + '/' + dir):
                    print('当前获取的文件完整路径：', user_path + domain + '/' + dir)

                    print('-------------------test2---------------------------')
                    print("领域名temp_domain_name：", temp_domain_name)
                    print("文件路径file_path：", user_path+domain+'/'+dir)
                    print('-------------------test2---------------------------')

                    try:
                        # 存放单个领域版本投产资料收集情况
                        all_check_report_dict=match_productionMaterials(request.session['user_name'],
                                                temp_domain_name,
                                                user_path+domain+'/'+dir)
                        print('所有领域版本投产资料收集情况：', all_check_report_dict)
                    except:
                        print('所有领域版本投产资料收集情况，配置中没有对应领域数据！')
                        continue

                    all_check_report_list.append(all_check_report_dict)

        date_list=sorted(date_list)
        print('当前所有投产日期：',date_list)
        # 读配置
        report_config = configparser.ConfigParser()
        report_config.read('config\\software_config\\report_check_list_config.ini', encoding='UTF-8')
        # 获取所有检查报告，不分前后端
        table_title = report_config.get('report_check_list', 'ALL')
        # 去空格
        table_title = table_title.strip()
        # 把字符串(配置)转换为列表
        table_title = table_title.split(',')
        table_title.insert(0, '版本号')
        return render(request, 'software/productionMaterials.html', locals())
    else:
        return render(request, 'software/ERROR.html')



def unblockedVersion(request):
    if not request.session.get('is_login', None):
        uploadFile_message = "您尚未登录，使用【解封版信息收集】请先登录！！"
        return render(request, 'software/index.html', locals())

    if request.method == "POST":
        newUnblocked_version=UnblockedVersionInfo.unblockedversion.create()
        newUnblocked_version.username=request.session['user_name']
        newUnblocked_version.month=request.POST.get('month')
        newUnblocked_version.team=request.POST.get('team')
        newUnblocked_version.version_number=request.POST.get('version_number')
        newUnblocked_version.subsystem=request.POST.get('subsystem')
        newUnblocked_version.version_name=request.POST.get('version_name')
        newUnblocked_version.content=request.POST.get('content')
        newUnblocked_version.version_compiler=request.POST.get('version_compiler')
        newUnblocked_version.version_leader=request.POST.get('version_leader')
        newUnblocked_version.test_leader=request.POST.get('test_leader')
        newUnblocked_version.development_team=request.POST.get('development_team')
        newUnblocked_version.version_type=request.POST.get('version_type')
        newUnblocked_version.unblocked_datetime=request.POST.get('unblocked_datetime')
        newUnblocked_version.blocked_datetime=request.POST.get('blocked_datetime')
        newUnblocked_version.unblocked_type=request.POST.get('unblocked_type')
        newUnblocked_version.unblocked_reason=request.POST.get('unblocked_reason')
        newUnblocked_version.save()

    # @register.filter
    # def get_range(value):
    #     return range(value)

    # 从数据库中查询当前登录用户的解封版所收集的信息
    unblocked_versionInfo_list = UnblockedVersionInfo.unblockedversion.filter(username=request.session['user_name'])
    return render(request, 'software/unblockedVersion.html', locals())


def modifySuperPWD(request):
    #修改二级密码
    if not request.session.get('is_login', None):
        return HttpResponse('<h4 style="color: red;font-weight: bold">您尚未登录普通用户，请先登录！！</h4>')

    modifyPassword = ModifySuperPWDForm()
    message = "修改二级密码"

    if request.method == "POST":
        username = request.session['user_name']
        #从数据库获取用户对象信息
        managers = ManagerDate.managers.get(user=request.session['user_name'])

        passwd_from=ModifySuperPWDForm(request.POST)
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


def modifyCardStatus(request):
    domain_list=['BRON','BRON-CLSS','BRON-CASS','BRON-CRMP','Python','jQuery','SQL','Bootstrap','Node.js','中文分类']

    # 获取领域名
    domain_name='BRON-CLSS'
    if request.GET.get('domain_name'):
        domain_name=request.GET.get('domain_name')
        print('domain_name: ', domain_name)

    if request.method == 'POST':
        if request.POST.get('sync'):
            sync_domain_by_waird = request.POST.get('sync')
            print('sync_domain_by_waird: ', sync_domain_by_waird)

        domain_name = request.POST.get('domain_name')
        print('domain_name: ', domain_name)


    branch_list=['BRON-CLSS1.1.0','BRON-CLSS1.2.0','BRON-CLSS1.3.0','BRON-CLSS1.4.0','BRON-CLSS1.5.0']
    date_form = ModifyCard()
    deldate_form = ModifyCard()

    # 获取停留在哪个功能页面
    if request.GET.get('feature'):
        myMenu = request.GET.get('feature')
    else:
        myMenu = request.POST.get('feature')
    print('myMenu: ',myMenu)
    if myMenu == 'myMenu0':
        myMenu0='select'
    elif myMenu == 'myMenu1':
        myMenu1 = 'select'
    elif myMenu == 'myMenu2':
        myMenu2 = 'select'
    elif myMenu == 'myMenu3':
        myMenu3 = 'select'
    elif myMenu == 'myMenu4':
        myMenu4 = 'select'
    elif myMenu == 'myMenu5':
        myMenu5 = 'select'
    else:
        myMenu5 = 'select'

    cardID = request.GET.getlist('cardID')
    print('cardID: ',cardID)

    return render(request, 'software/modifyCardStatus.html', locals())


def test(request):
    path = 'config\\software_config\\report_check_list_config2.ini'
    try:
        config_1=getConfig(path)
        print('-----------------------------------------------------------------1')
        # print(config_1.get_items('report_check_list'))
        # print('-----------------------------------------------------------------2')
        # print(config_1.check_section('report_check_list'))
        # print('-----------------------------------------------------------------3')
        # print(config_1.check_key('report_check_list','ALL'))
        # print('-----------------------------------------------------------------4')
        # print(config_1.check_value('report_check_list','ALL','发布检查单qwe'))
        # print('-----------------------------------------------------------------5')
        print(config_1.add_section('yinjinpei'))
        # print('-----------------------------------------------------------------6')
        # print(config_1.set_section('user','b','2'))
        # print(config_1.set_section('user', 'c', '4'))
        # print('-----------------------------------------------------------------7')
        # print(config_1.remove_key('user','b'))
        print(config_1.save())
        # print('-----------------------------------------------------------------8')
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


def test_job():
    for i in range(5):
        t_now = time.localtime()
        print(t_now)

def test_job2():
    for i in range(5):
        print('正在执行任务中。。。')

def timed_task(request):
    try:
        # 调度器使用DjangoJobStore()
        # scheduler.add_jobstore(DjangoJobStore(), "default")

        # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
        # ('scheduler',"interval", seconds=1) #用interval方式循环，每一秒执行一次
        # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10', id='task_time')

        scheduler.add_job(test_job, trigger='interval', id='test_job3', minutes=1, next_run_time=datetime.datetime.now(),
                          coalesce=True, misfire_grace_time=3000, start_date='2020-10-30 22:12:11',
                          end_date='2020-11-26 23:00:00', replace_existing=True)
        scheduler.add_job(test_job2, trigger='interval', id='test_job4', minutes=1, next_run_time=datetime.datetime.now(),
                          coalesce=True, misfire_grace_time=3000, start_date='2020-10-30 22:12:11',
                          end_date='2020-11-26 23:00:00', replace_existing=True)
        # 调度器开始
        # scheduler.start()

    except Exception as e:
        print(e)
        # 报错则调度器停止执行
        # scheduler.shutdown()

    print(scheduler.get_job(job_id='test_job'))
    return HttpResponse(scheduler.get_job(job_id='test_job'))

def test2(request,file_path=None,domain_name=None,password=None):
    file_path='uploads/shar/BRON-CLSS（车主生活服务子系统）/BRON-CLSS1.0.0（2020-05-20）'
    domain_name='BRON-CLSS'

    '''文件分类 starting'''
    # 获取版本号,BRON-COSS1.2.0
    version = file_path.split('/')[-1].split('（')[0]
    if version is None:
        version = domain_name

    # 获取版本号带日期，BRON-COSS1.2.0（2020-10-30）
    planName_data = file_path.split('/')[-1]
    print('带版本日期：', planName_data)
    if planName_data is None:
        planName_data = domain_name

    # 获取所有文件名
    file_list = os.listdir(file_path)
    file_list_temp = os.listdir(file_path)
    if len(file_list) == 0:
        return False

    # 获取领域所需要检查的报告
    getMatchKeywords = getConfig('config\\software_config\\report_check_list_config.ini')

    # 获取所有检查报告，不分前后端
    all_check_report = getMatchKeywords.get_value('report_check_list', 'all')
    # 去空格
    all_check_report = all_check_report.strip()
    # 把字符串(配置)转换为列表
    all_check_report = all_check_report.split(',')

    print('---------------------------------------------------')
    print('%s检查报告列表：%s' % (domain_name, all_check_report))
    print('---------------------------------------------------')

    # 创建临时目录
    tempDir = planName_data + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%H%S')
    tempDir = tempDir.replace(' ','')
    targetPath = 'uploads\\temp'

    sourcePath = targetPath + '\\' + tempDir
    if os.path.exists(targetPath):
        os.mkdir(sourcePath)
    else:
        os.makedirs(sourcePath)
    print('创建分类zip打包临时目录：',sourcePath)

    for report in all_check_report:
        # 创建分类目录
        # print('创建分类目录：',sourcePath + '\\' + report)
        os.mkdir(sourcePath + '\\' + report)
        try:
            findStr = getMatchKeywords.get_value('match_keywords', report)
            print('%s 的匹配关键字：'%report,findStr)
        except Exception as e:
            print(e)
            print('本次匹配没有匹配到对应的报告类型！')
            continue

        print('文件列表：',file_list)
        for file in file_list:
            matchStr = re.findall(findStr, str(file), re.M | re.I | re.S)
            if matchStr:
                # print('拷贝目标路径: ',file_path+'\\'+str(file),sourcePath+'\\'+report+'\\'+str(file))
                # 拷贝文件和状态信息
                shutil.copy2(file_path+'\\'+str(file),sourcePath+'\\'+report+'\\'+str(file))
                print('【%s】报告已拷贝到【%s】目录！' % (file, report))
                file_list_temp.remove(file)
    else:
        os.mkdir(sourcePath + '\\' + '其他')
        # print('创建分类目录：', sourcePath + '\\' + '其他')

    for file in file_list_temp:
        shutil.copy2(file_path + '\\' + str(file), sourcePath + '\\' + '其他' + '\\' + str(file))
        print('【%s】报告已拷贝到【其他】目录！' % file)

    '''文件分类 end'''

    '''打包--未加密 starting'''
    source_dir = sourcePath
    output_dir = targetPath
    output_filename = tempDir + '.zip'
    make_zip(source_dir, output_dir, output_filename)
    '''打包--未加密 end'''

    # '''打包 starting'''
    # outFullName=sourcePath+planName_data'+'.zip'
    # password='123'
    # isSuccessful = zipDir(sourcePath, outFullName, password)
    # if isSuccessful == True:
    #     print('zip打包成功！' )
    # else:
    #     print('zip打包失败！')
    # '''加密打包 end'''

    return HttpResponse('哈哈')

