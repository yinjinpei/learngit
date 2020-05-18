# coding:utf-8
import os
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
from django.core.files.temp import NamedTemporaryFile
# Django不支持range函数
from django.template.defaulttags import register
import ast
import logging
# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

# 黑名单目录下不显示上传功能
black_user_list=['shar', 'tdc', 'igmh']

#白名单可访问投产材料管理页面
allow_users_list=['shar', 'tdc',]

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

def downloadFileInfo(path):
    fileObjectList = [] # 存放文件对象
    dirObjectList = []  # 存放目录对象

    fileList = os.listdir(path)

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
            filepath = path + file
            print('文件完整路径：【%s】' % filepath)

            fileSize = os.path.getsize(filepath)  # 获取文件大小
            fileSize = fileSize / float(1024)
            fileSize = round(fileSize, 2)

            fileCreatTime = os.path.getctime(filepath)  # 获取文件创建时间
            fileCreatTime = datetime.datetime.fromtimestamp(fileCreatTime)
            fileCreatTime = fileCreatTime.strftime('%Y-%m-%d %X')

            fileObject = DownloadFileObject(file, fileSize, fileCreatTime, path)  # 创建文件对象
            fileObjectList.append(fileObject)  # 把文件对象存放到列表

        elif os.path.isdir(path + file):
            print('【%s】：这是一个目录' % file)
            dirObject=AbsolutePath(file, path + file)
            dirObjectList.append(dirObject)
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


def match_productionMaterials(user_name,domain_name,file_path):
    '''
    :param user_name: 登录用户名
    :param domain_name: 领域名
    :param file_path: 文件的完整路径
    :return: 返回字典
    '''
    # 获取所有文件名
    file_list = os.listdir(file_path)
    # 获取数据库领域所有数据，理论上数据库只有一条，返回的值是列表形式
    domainInfo_list = DomainInfo.domains.filter(user_name=user_name,isDelete=False, domain_name=domain_name)
    print('------------------------------------------------')
    print(domainInfo_list)
    print('------------------------------------------------')
    if len(domainInfo_list) == 0:
        return False
    # 存放相关测试报告项，且需要字符串转成字典，使用 ast模块
    version_data_dict = ast.literal_eval(domainInfo_list[0].version_data)
    print(type(version_data_dict))
    print(version_data_dict)

    # 获取所有values
    title_list=[]
    for title in version_data_dict.values():
        title_list.append(title)
    print('**************************************************')
    print(title_list)
    print('**************************************************')
    # 获取所有key,即测试报告类型，如需求说明书的key:demand_doc，发布检查单的key:checklist
    version_data_dict_key_list = version_data_dict.keys()
    key_list = []
    value_list = []
    for report_type in version_data_dict_key_list:
        print('-----------------------------------')
        print(report_type)
        print(version_data_dict[report_type])
        print('-----------------------------------')
        file_exist = ('X')
        for file_name in file_list:
            try:
                matchStr = re.match("(.*)%s(.*)" % version_data_dict[report_type], str(file_name), re.M | re.I)
                print("存在的材料：", matchStr.group())
                file_exist = '✔'
                break
            except:
                continue
        value_list.append(file_exist)
        key_list.append(report_type)

    print(key_list)
    print(value_list)

    # 返回投产材料检查后的结果，检查名和其值（存在：✔  不存在：X ）
    return title_list,value_list

def delFile(request):
    versionManagerUsers = black_user_list
    print('删除文件')
    if request.method == "POST":
        user_home = 'uploads/' + request.session['user_name'] + '/'
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        print('删除文件使用POST方式')

        dirname = request.GET.get('dirname')
        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]

            path=dirname+'/'
        print('~~~~~~~~~~~~~~~dirname：', dirname)

        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'

        downloadFileName = request.POST.get('downloadFileName')
        print('===================----------------=======================')
        print(downloadFileName)
        print('===================----------------=======================')
        if downloadFileName is not None:
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
                            title_list, value_list = match_productionMaterials(request.session['user_name'],
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
                                title_list, value_list = match_productionMaterials(request.session['user_name'],
                                                                                   domain_name, file_path)
                            except:
                                pass

            path = dirname + '/'

            FileName = delFile_form.cleaned_data['FileName']    # 获取删除的文件名
            if os.path.exists(path+FileName):
                os.remove(path+FileName)
                delfile_message="【%s】 删除成功！！"%FileName
            else:
                delfile_message = "【%s】 文件不存在，删除失败！！" % FileName

        fileObjectList, dirObjectList= downloadFileInfo(path)

        delFile_form = DelFile()
        return render(request, 'software/uploadFile.html', locals())
    else:
        # return HttpResponse('<h4 style="color: red;font-weight: bold">删除文件后请勿刷新，回退一步或重新打开即可！</h4>')
        user_home = 'uploads/' + request.session['user_name'] + '/'
        path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        print('删除文件使用POST方式')

        dirname = request.GET.get('dirname')

        if dirname:
            up_one_level_path = up_one_level(dirname)
            dirList_is_not_null = '在模板显示返回上一层，仅作标志'

        if dirname:
            if dirname[-1] == '/':
                dirname = dirname[:-1]

            if request.session['user_name'] in versionManagerUsers:
                if len(dirname.split('/')) == 4:
                    print('******************** 不是空值 ********************')
                    domain_name = dirname.split('/')[2]
                    file_path = dirname
                    try:
                        title_list, value_list = match_productionMaterials(request.session['user_name'],
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

    # 版本管理用户
    versionManagerUsers = black_user_list

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

    print('###############################################获取到的绝对路径dirname：',dirname)
    if dirname is not None:
        if dirname[-1] == '/':
            dirname = dirname[:-1]

        if request.session['user_name'] in versionManagerUsers:
            if len(dirname.split('/')) == 4:
                domain_name=dirname.split('/')[2]
                file_path=dirname
                try:
                    title_list, value_list=match_productionMaterials(request.session['user_name'],domain_name,file_path)
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
        if request.session['user_name'] != 'shar':
            dirname=path[:-1]

    fileObjectList, dirObjectList = downloadFileInfo(path)

    # 判断上传是否为空
    try:
        request.FILES['file']
    except:
        message = '温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        return render(request, 'software/uploadFile.html', locals())

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

        uploadFileList=request.FILES.getlist('file') # 获取所有上传的文件对象
        print('************************所有上传的文件对象**************************')
        print(uploadFileList)
        print('******************************************************************')

        repeatFileList = [] # 记录重名的文件名
        upload_list_successful=[] # 记录上传成功的文件名
        repeatFileSum=0 # 重名文件的总个数

        for file in uploadFileList:
            print(len(uploadFileList))
            fileName=str(file) # 上传的文件名
            print("================== 文件名%s============="%file)
            file=request.FILES['file']  #上传的文件对象
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
        message='温馨提示：可直接用鼠标拖拉多个文件到框框内，鼠标停放框内查看已选择的文件！'
        print(message)

    fileObjectList, dirObjectList = downloadFileInfo(path)

    return render(request, 'software/uploadFile.html', locals())


# def downloadFile(request,fileObject=None,filename=None):
#
#     # 用于全部文件下载功能
#     if fileObject is None and filename is None:
#         # 获取上传文件路径和文件名
#         fileObject = request.POST.get('name')
#         # 提取文件名
#         tmp_list =fileObject.split('/')
#         filename = tmp_list[-1]
#
#     print('000000000000000000000000000000000')
#     print('文件名：',filename)
#     print('完整的路径：',fileObject)
#     print('000000000000000000000000000000000')
#     try:
#         file = open(fileObject,'rb')
#     except:
#         return HttpResponse('下载文件名有错，请联系管理员！  文件名：%s'%fileObject)
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/octet-stream'
#     # response['Content-Disposition'] = "attachment;filename=%s"%filename #下载带中文文件名时会有乱码，解决如下：
#     response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
#         # IE浏览器，采用URLEncoder编码
#         # Opera浏览器，采用filename * 方式
#         # Safari浏览器，采用ISO编码的中文输出
#         # Chrome浏览器，采用Base64编码或ISO编码的中文输出
#         # FireFox浏览器，采用Base64或filename * 或ISO编码的中文输出
#     return response


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

    if request.method == "POST":
        dirname = request.POST.get('dirname')
        print('dirname POST方式传递过来的值:', dirname)

        newDirectory_form = NewDirectory(request.POST)
        if newDirectory_form.is_valid():  # 如果有数据
            DirectoryName = newDirectory_form.cleaned_data['DirectoryName'] # 获取新建文件夹名
            try:
                os.makedirs(dirname+DirectoryName)
                message="%s 创建目录成功！"%(dirname+DirectoryName)
            except:
                message = "%s 创建目录失败，请检查目录是否已存在！" % (dirname+DirectoryName)
            print(message)

    newDirectory_form=NewDirectory()
    return render(request, 'software/newDirectory.html', locals())


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
        uploadFile_message = "您尚未登录，使用【修改服务器时间】请先登录！！"
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
                    def __init__(self, serverIP, username, password, commond, port=22):
                        self.serverIP = serverIP
                        self.username = username
                        self.password = password
                        self.port = port
                        self.setdatetime = commond
                    # SSH连接服务器，用于命令执行
                    def ssh_connectionServer(self):
                        print(self.serverIP)
                        print(self.username)
                        print(self.password)
                        print(self.port)
                        set_time = 'date -s "%s"' % (self.setdatetime)
                        print(set_time)

                        try:
                            print('创建SSH对象--------')
                            # 创建SSH对象
                            sf = paramiko.SSHClient()
                            # 允许连接不在know_hosts文件中的主机
                            sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            print('开始连接服务器')
                            # 连接服务器
                            sf.connect(hostname=self.serverIP, port=self.port, username=self.username,
                                       password=self.password)
                            print('连接服务器成功！')

                            # 注意：依次执行多条命令时，命令之间用分号隔开
                            stdin, stdout, stderr = sf.exec_command(set_time)
                            result = stdout.read().decode('utf-8')
                            print("命令执行成功！\n结果如下：\n%s" % result)
                            time.sleep(3)
                            stdin, stdout, stderr = sf.exec_command('date')
                            result = stdout.read().decode('utf-8')
                            print("命令执行成功！\n结果如下：\n%s" % result)
                        except:
                            print("连接服务器：" + self.serverIP + " 失败了!")
                            return False
                        return True

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


# @accept_websocket
# def exec_command(request):
#     if not request.is_websocket():  # 判断是不是websocket连接
#         try:  # 如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render(request, 'software/exec_command.html')
#     else:
#         for message in request.websocket:
#             print(request.is_websocket)
#             print(message)
#             message = message.decode('utf-8')  # 接收前端发来的数据
#             print(message)
#             if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
#                 command = 'bash /opt/test.sh'  # 这里是要执行的命令或者脚本
#
#                 # 远程连接服务器
#                 hostname = '192.168.0.200'
#                 username = 'root'
#                 password = '123456'
#
#                 ssh = paramiko.SSHClient()
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#                 ssh.connect(hostname=hostname, username=username, password=password)
#                 # 务必要加上get_pty=True,否则执行命令会没有权限
#                 print('开始执行命令')
#                 stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
#                 message = stdout.read()  # 读取脚本输出内容
#                 request.websocket.send(message)  # 发送消息到客户端
#                 print(message.decode('utf-8'))
#
#                 # 循环发送消息给前端页面
#                 # while True:
#                 #     print('开始打印')
#                 #     message = stdout.readline().strip()  # 读取脚本输出内容
#                 #     request.websocket.send(message)  # 发送消息到客户端
#                 #     # 判断消息为空时,退出循环
#                 #     print('打印结束')
#                 #     if not message:
#                 #         break
#                 # ssh.close()  # 关闭ssh连接
#                 # print('ssh连接结束！')
#
#                 break
#             else:
#                 request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
#
# @accept_websocket
# def websocket_test(request):
#     if not request.is_websocket():  # 判断是不是websocket连接
#         try:  # 如果是普通的http方法
#             message = request.GET['message']
#             print(message)
#             return HttpResponse(message)
#         except:
#             return render(request, 'software/websocker_test.html')
#     else:
#         for message in request.websocket:
#             request.websocket.send(message)#发送消息到客户端


def test(request):
    return render(request, 'test.html', locals())


def productionMaterials(request):
    # 访问此功能的白名单用户
    allow_users=allow_users_list
    user_dir_list=[]
    if request.session['user_name'] in allow_users:
        user_path = 'uploads/' + request.session['user_name'] + '/'  # 下载文件路径，相对路径，在项目根目录下
        for dir in os.listdir(user_path):
            print(dir)
            print(user_path+dir)
            if os.path.isdir(user_path+dir):
                temp_domain_name=dir.split('（')
                user_dir_list.append(temp_domain_name)
        print(user_dir_list)

        if request.method == "GET":
            dirname=request.GET.get('domain')
            print(dirname,'88888888888888888888')

            if dirname:
                version_dir_list=[]
                version_path = 'uploads/' + request.session['user_name'] + '/' + dirname +'/'
                print('当前路径：',version_path)
                for dir in os.listdir(version_path):
                    print('当前目录：',dir)
                    if os.path.isdir(version_path+dir):
                        version_dir_list.append(dir)

        if request.method == "POST":
            # 获取目录，如：BCOS-MNGT/BCOS-MNGT1.1.0（2020-05-10）
            version_name=request.POST.get('version_name')
            # 获取领域名
            domain_name = version_name.split('/')[0]
            # 获取完整路径，如：uploads/shar/BCOS-MNGT/BCOS-MNGT1.1.0（2020-05-10）
            file_path = user_path+version_name
            # 获取文件目录名,如：BCOS-MNT1.1.0（2020-05-14）
            domain_path=version_name.split('/')[1]
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
            print("领域名：", domain_name)
            print("当前目录名：",domain_name)
            print("文件路径：",file_path)
            print('-------------------test1---------------------------')

            # title_list=['发版检查单','需求说明书','需求评审','安全评审','代码评审','SIT测试报告','UAT测试报告',
            #             '安全测试报告','代码安全扫描报告','代码质量扫描报告','SQM审核报告','DBA评审报告','回归测试报告']
            try:
                title_list,value_list=match_productionMaterials(request.session['user_name'],domain_name,file_path)
            except:
                print('数据库中没有对应领域数据！')
        # 存放所有领域版本投产资料收集情况
        domain_values_list=[]

        # 遍历用户下面所有领域，并检查投产材料收集情况
        for domain in user_dir_list:
            print(domain)
            for dir in os.listdir(user_path+domain): # 获取用户下所有领域目录和文件
                if os.path.isdir(user_path + domain + '/' + dir):
                    try:
                        title, values=match_productionMaterials(request.session['user_name'],
                                                domain,
                                                user_path+domain+'/'+dir)
                        print('当前获取的文件完整路径：',user_path+domain+'/'+dir)
                        # 获取版本号目录
                        version_dir_name=dir.split('（')[0]
                        info=[version_dir_name, title, values]
                        domain_values_list.append(info)
                    except:
                        print('数据库中没有对应领域数据！')
        print('所有领域版本投产资料收集情况：',domain_values_list)


        return render(request, 'software/productionMaterials.html', locals())
    else:
        return render(request, 'software/ERROR.html')



def unblockedVersion(request):
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

