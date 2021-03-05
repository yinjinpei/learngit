# coding:utf-8
from django.db import models
from django import forms
import datetime

# Create your models here.
class AppInfo(models.Model):
    userName = models.CharField(max_length=128, default=None)
    appName = models.CharField(max_length=20)
    appDir = models.CharField(max_length=100)
    remark = models.CharField(max_length=100,default=None)
    isDelete = models.BooleanField(default=False)
class Meta():
    db_table='appinfo'
    apps = models.Manager()
    def showname(self):
        return self.appName
    def showdir(self):
        return self.appDir
    def showID(self):
        return self.pk
    def showusername(self):
        return self.userName

class AddSoftware(forms.Form):
    ChineseName = forms.CharField(label="应用中文名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    EnglishName = forms.CharField(label="应用英语名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    SoftwarePath = forms.CharField(label="应用启动路径", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

class DelSoftware(forms.Form):
    ChineseName = forms.CharField(label="应用中文名", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))

class DelFile(forms.Form):
    FileName = forms.CharField(label="输入完整的文件名可直接删除", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))

class NewDirectory(forms.Form):
    DirectoryName = forms.CharField(label="目录名", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateDirectory(forms.Form):
    englishName = forms.CharField(label="英文简称", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    chineseName = forms.CharField(label="中文名称", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateVersionDirectory(forms.Form):
    VersionName = forms.CharField(label="版本号", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'输入版本号'}))
    Date = forms.DateField(label='投产日期', widget=forms.DateInput(attrs={'class': 'weui-input','type': 'date'}))

class DateForm(forms.Form):
    ServerIP = forms.CharField(label="服务器的IP", max_length=128, widget=forms.TextInput(attrs={'class': 'serverip'}))
    # 实现可选的日期输入格式
    # Date = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type': 'date'}))
    Datetime = forms.DateTimeField(initial=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),label='日期和时间', input_formats=['%Y-%m-%dT%H:%M'],
                                   widget=forms.DateTimeInput(attrs={'class': 'weui-input',
                                                                     'type': 'datetime-local',
                                                                     'emptyTips': '请选择时间'}))
    ServerDatetime = forms.DateTimeField(initial=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'),label='日期和时间', input_formats=['%Y-%m-%dT%H:%M'],
                                         widget=forms.DateTimeInput(attrs={'class': 'weui-input',
                                                                           'type': 'datetime-local',
                                                                           'emptyTips': '请选择时间'}))

class ModifyCard(forms.Form):
    Datetime = forms.DateTimeField(initial=datetime.datetime.now().strftime('%Y-%m-%dT00:00'),label='日期和时间', input_formats=['%Y-%m-%dT%H:%M'],
                                   widget=forms.DateTimeInput(attrs={'class': 'weui-input',
                                                                     'type': 'datetime-local',
                                                                     'emptyTips': '请选择时间'}))

class DelForm(forms.Form):
    MyJobID = forms.CharField(label="线程ID", max_length=128, widget=forms.TextInput(attrs={'class': 'myjobid'}))

class TimingData(models.Model):
    execTime = models.DateTimeField()
    setTime = models.DateTimeField()
    serverIP = models.CharField(max_length=20)
    clientJobID=models.CharField(max_length=128)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table='timingdata'

    timers = models.Manager()
    def showexectime(self):
        return self.execTime
    def showsetTime(self):
        return self.setTime
    def showserverIP(self):
        return self.serverIP
    def showclientJobID(self):
        return self.clientJobID
    def showID(self):
        return self.pk
    def showisDelete(self):
        return self.isDelete

class DomainInfo(models.Model):
    # 领域名,unique为不允许重复
    domain_name = models.CharField(max_length=128, unique=True)
    # 领域负责人邮箱
    domain_manager_email = models.EmailField()
    # 测试负责人邮箱
    test_manager_email = models.EmailField()
    # 开发团队邮箱群
    domain_team_email = models.EmailField()
    # 版本经理邮箱
    version_manager_email = models.EmailField()
    #用户
    user_name = models.CharField(max_length=128)
    # 版本投产材料
    version_data = models.CharField(max_length=1024)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)
    # # 投产日期
    # plan_start_date = models.DateField()
    # # 版本号
    # version = models.CharField(max_length=256)
    # 版本经理邮箱
    # version_manager_email = models.EmailField(unique=True)
    # # 版本检查清单
    # checklist = models.CharField(max_length=128, unique=True)
    # # 需要文档
    # demand_doc = models.CharField(max_length=128, unique=True)
    # # 需要评审
    # demand_review = models.CharField(max_length=128, unique=True)
    # # 安全评审
    # safety_review = models.CharField(max_length=128, unique=True)
    # # 代码评审
    # code_review = models.CharField(max_length=128, unique=True)
    # # sit测试报告
    # sit_report = models.CharField(max_length=128, unique=True)
    # # uat测试报告
    # uat_report = models.CharField(max_length=128, unique=True)
    # # 安全报告
    # safety_report = models.CharField(max_length=128, unique=True)
    # # 代码安全扫描报告
    # code_security_scan_report = models.CharField(max_length=128, unique=True)
    # # 代码质量扫描报告
    # code_quality_scan_report = models.CharField(max_length=128, unique=True)
    # # SQM审核报告
    # sqm_report = models.CharField(max_length=128, unique=True)
    # # DBA脚本评审报告
    # dba_review = models.CharField(max_length=128, unique=True)
    # # 回归测试报告
    # regress_review = models.CharField(max_length=128, unique=True)
    # # 生产验证报告
    # verification_review = models.CharField(max_length=128, unique=True)
class Meta:
    db_table = 'domaininfo'

    def __str__(self):
        return self.domain_name

    domains = models.Manager()
    def show_domain_name(self):
        return self.domain_name
    def show_domain_manager_email(self):
        return self.domain_manager_email
    def show_test_manager_email(self):
        return self.test_manager_email
    def show_domain_team_email(self):
        return self.domain_team_email
    def show_version_manager_email(self):
        return self.version_manager_email
    def show_user_name(self):
        return self.user_name
    def show_version_data(self):
        return self.version_data
    def show_isDelete(self):
        return self.isDelete

class UnblockedVersionInfo(models.Model):
    # 登录用户名
    username = models.CharField(max_length=128)
    # 月份
    month = models.CharField(max_length=128)
    # 团队
    team = models.CharField(max_length=128)
    # 版本号
    version_number = models.CharField(max_length=128)
    # 子系统名称
    subsystem = models.CharField(max_length=128)
    # 版本名称
    version_name = models.CharField(max_length=128)
    # 版本内容
    content = models.CharField(max_length=512)
    # 版本编制人
    version_compiler =models.CharField(max_length=128)
    # 开发负责人
    version_leader = models.CharField(max_length=128)
    # 测试负责人
    test_leader = models.CharField(max_length=128)
    # 所属开发组
    development_team = models.CharField(max_length=128)
    # 版本类型
    version_type = models.CharField(max_length=128)
    # 申请解封时间
    unblocked_datetime = models.CharField(max_length=128)
    # 确认封版时间
    blocked_datetime = models.CharField(max_length=128)
    # 解封版类别
    unblocked_type= models.CharField(max_length=128)
    # 解封版说明及根因分析
    unblocked_reason = models.CharField(max_length=1024)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'unblockedversionInfo'

    unblockedversion = models.Manager()
    def show_ID(self):
        return self.pk

    def show_username(self):
        return self.username

    def show_month(self):
        return self.month

    def show_team(self):
        return self.team

    def show_version_number(self):
        return self.version_number

    def show_subsystem(self):
        return self.subsystem

    def show_version_name(self):
        return self.version_name

    def show_content(self):
        return self.content

    def show_version_compiler(self):
        return self.version_compiler

    def show_version_leader(self):
        return self.version_leader

    def show_test_leader(self):
        return self.test_leader

    def show_version_type(self):
        return self.version_type

    def show_unblocked_datetime(self):
        return self.unblocked_datetime

    def show_blocked_datetime(self):
        return self.blocked_datetime

    def show_unblocked_type(self):
        return self.unblocked_type

    def show_unblocked_reason(self):
        return self.unblocked_reason

    def show_isDelete(self):
        return self.isDelete

class ManagerForm(forms.Form):
    password = forms.CharField(label="二级密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label="首次登录，设置二级密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="再次输入，确认二级密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ModifySuperPWDForm(forms.Form):
    password = forms.CharField(label="输入原有密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="设置新的二级密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="再次输入，确认新的二级密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ManagerDate(models.Model):
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    class Meta():
        db_table='managerdate'

    managers = models.Manager()
    def showUser(self):
        return self.user
    def showPassword(self):
        return self.password

class LockBaseInfo(models.Model):
    userName= models.CharField(max_length=20, default=None)
    pathName = models.CharField(max_length=128)
    islock = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table='lockbaseinfo'
    lockbase = models.Manager()

class PrdDataBaseInfo(models.Model):
    # 当前登录用户名
    loginUser = models.CharField(max_length=128)
    # 所属团队
    blongTo = models.CharField(max_length=128)
    # 领域名
    domain = models.CharField(max_length=128)
    # 数据库串
    dataBaseLink = models.CharField(max_length=128)
    # 数据库名
    dataBaseName = models.CharField(max_length=128)
    # 数据库用户名
    userName = models.CharField(max_length=128)
    # 备注
    remark = models.CharField(max_length=128)
    # 环境类型
    envType = models.CharField(max_length=128)
    # 修改时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'prdDataBaseInfo'
    prddatabase = models.Manager()

class UatDataBaseInfo(models.Model):
    # 当前登录用户名
    loginUser = models.CharField(max_length=128)
    # 所属团队
    blongTo = models.CharField(max_length=128)
    # 领域名
    domain = models.CharField(max_length=128)
    # 数据库串
    dataBaseLink = models.CharField(max_length=128)
    # 数据库名
    dataBaseName = models.CharField(max_length=128)
    # 数据库用户名
    userName = models.CharField(max_length=128)
    # 备注
    remark = models.CharField(max_length=128)
    # 环境类型
    envType = models.CharField(max_length=128)
    # 修改时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'uatDataBaseInfo'
    uatdatabase = models.Manager()

class TimedTaskForMoveCard(models.Model):
    # 用户名
    userName = models.CharField(max_length=128)
    # 领域名
    domainName = models.CharField(max_length=128)
    # 神兵空间英文简称
    zoneName = models.CharField(max_length=128)
    # 分支
    branch = models.CharField(max_length=128)
    # gitlab项目id
    projectId = models.CharField(max_length=128)
    # 任务开始时间
    startTime = models.DateTimeField()
    # 任务结束时间
    endTime = models.DateTimeField()
    # 时间间隔
    intervalTime = models.IntegerField()
    # 时间单位
    timeType = models.CharField(max_length=128)
    # 任务id
    taskId =  models.IntegerField(default=None)
    # 任务状态
    taskStatus = models.CharField(max_length=128, default=None)
    # 任务对象
    taskObject = models.CharField(max_length=128,default=None)
    # 此条数据是否已被删除
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'timedTaskForMoveCard'
    timedTask = models.Manager()

class ApplicantDeploymentInfo(models.Model):
    # 用户名
    loginUser = models.CharField(max_length=128)
    # 系统名称
    systemName = models.CharField(max_length=128)
    # 系统类型
    systemType = models.CharField(max_length=128)
    # 申请人
    applicant = models.CharField(max_length=128)
    # 申请时间
    applicantTime = models.CharField(max_length=128)
    # 原因分类
    reasonType = models.CharField(max_length=128,null=True)
    # 申请原因
    reason = models.CharField(max_length=256)
    # 编辑时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'applicantDeploymentInfo'
    applicantDeployment = models.Manager()

class SelfDeploymentInfo(models.Model):
    # 用户名
    loginUser = models.CharField(max_length=128)
    # 系统名称
    systemName = models.CharField(max_length=128)
    # 部署执行人角色
    role = models.CharField(max_length=128, null=True)
    # 部署执行人
    deploymentPersonnel = models.CharField(max_length=128)
    # 部署时间
    deploymentTime = models.CharField(max_length=128)
    # 编辑时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'selfDeploymentInfo'
    selfDeployment = models.Manager()

class MyServerInfo(models.Model):
    # 用户名
    loginUser = models.CharField(max_length=128)
    # 所属团队
    blongTo = models.CharField(max_length=128)
    # 领域名
    domainName = models.CharField(max_length=128)
    # 环境类型
    envType = models.CharField(max_length=128)
    # 应用APPID
    appid = models.CharField(max_length=128)
    # IP地址
    ip = models.CharField(max_length=128)
    # 应用名
    applicantName = models.CharField(max_length=128)
    # 应用类型
    applicantType = models.CharField(max_length=128)
    # 部署平台
    deployPlatform = models.CharField(max_length=128)
    # 备注
    remark = models.CharField(max_length=128)
    # 更新时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'myServerInfo'
    myServer = models.Manager()

class MyGitlabInfo(models.Model):
    # 用户名
    loginUser = models.CharField(max_length=128)
    # 所属团队
    blongTo = models.CharField(max_length=128)
    # 插件英文名称
    packageName = models.CharField(max_length=128)
    # 应用APPID
    appid = models.CharField(max_length=128)
    # gitlab地址
    gitlabBase = models.CharField(max_length=128)
    # gitlab项目ID
    projectId = models.CharField(max_length=128)
    # 绑定空间
    wizardSpace = models.CharField(max_length=128)
    # 子系统
    system = models.CharField(max_length=128)
    # 开发负责人
    person = models.CharField(max_length=128)
    # 类型（仅前端）
    type = models.CharField(max_length=128)
    # 备注
    remark = models.CharField(max_length=128)
    # 更新时间
    modifyTime = models.CharField(max_length=128)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'myGitlabInfo'
    myGitlab = models.Manager()

class NewUnblockedVersionInfo(models.Model):
    # 登录用户名
    username = models.CharField(max_length=128)
    # 月份
    month = models.CharField(max_length=128)
    # 领域
    team = models.CharField(max_length=128)
    # 版本名称
    version_name = models.CharField(max_length=128)
    # 子系统名称
    subsystem = models.CharField(max_length=128)
    # 版本需求
    content = models.CharField(max_length=1024)
    # 版本经理
    version_manager =models.CharField(max_length=128)
    # 开发负责人
    version_leader = models.CharField(max_length=128)
    # 测试负责人
    test_leader = models.CharField(max_length=128)
    # 版本类型
    version_type = models.CharField(max_length=128)
    # 解封开始时间
    unblocked_datetime = models.CharField(max_length=128)
    # 封版时间
    blocked_datetime = models.CharField(max_length=128)
    # 解封版类别
    unblocked_type= models.CharField(max_length=128)
    # 解封版说明及根因分析
    unblocked_reason = models.CharField(max_length=2048)
    # 备注
    remark = models.CharField(max_length=1024)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'newunblockedversionInfo'

    newunblockedversion = models.Manager()