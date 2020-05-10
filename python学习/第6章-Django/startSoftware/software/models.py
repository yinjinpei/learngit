# coding:utf-8
from django.db import models
from django import forms

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
    DirectoryName = forms.CharField(label="请输入目录名称", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))


class DateForm(forms.Form):
    ServerIP = forms.CharField(label="服务器的IP", max_length=128, widget=forms.TextInput(attrs={'class': 'serverip'}))
    # 实现可选的日期输入格式
    # Date = forms.DateField(label='日期', widget=forms.DateInput(attrs={'type': 'date'}))
    Datetime = forms.DateTimeField(label='日期和时间', input_formats=['%Y-%m-%dT%H:%M'],
                                   widget=forms.DateTimeInput(attrs={'class': 'weui-input',
                                                                     'type': 'datetime-local',
                                                                     'emptyTips': '请选择时间'}))
    ServerDatetime = forms.DateTimeField(label='日期和时间', input_formats=['%Y-%m-%dT%H:%M'],
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


class VersionInfo(models.Model):
    # 领域名
    domain_name = models.CharField(max_length=128, unique=True)
    # 版本号
    version = models.CharField(max_length=256)
    # 投产日期
    plan_start_date = models.DateField(auto_now_add=True)
    # 领域负责人邮箱
    domain_manager_email = models.EmailField(unique=True)
    # 测试负责人邮箱
    test_manager_email = models.EmailField(unique=True)
    # 开发团队邮箱群
    domain_team_email = models.EmailField(unique=True)
    # 版本经理邮箱
    version_manager_email = models.EmailField(unique=True)
    # 版本检查清单
    checklist = models.CharField(max_length=128, unique=True)
    # 需要文档
    demand_doc = models.CharField(max_length=128, unique=True)
    # 需要评审
    demand_review = models.CharField(max_length=128, unique=True)
    # 安全评审
    safety_review = models.CharField(max_length=128, unique=True)
    # 代码评审
    code_review = models.CharField(max_length=128, unique=True)
    # sit测试报告
    sit_report = models.CharField(max_length=128, unique=True)
    # uat测试报告
    uat_report = models.CharField(max_length=128, unique=True)
    # 安全报告
    safety_report = models.CharField(max_length=128, unique=True)
    # 代码安全扫描报告
    code_security_scan_report = models.CharField(max_length=128, unique=True)
    # 代码质量扫描报告
    code_quality_scan_report = models.CharField(max_length=128, unique=True)
    # SQM审核报告
    sqm_report = models.CharField(max_length=128, unique=True)
    # DBA脚本评审报告
    dba_review = models.CharField(max_length=128, unique=True)
    # 回归测试报告
    regress_review = models.CharField(max_length=128, unique=True)
    # 生产验证报告
    verification_review = models.CharField(max_length=128, unique=True)
    # 数据是否被已弃用
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = 'versioninfo'

    def __str__(self):
        return self.name
    domains = models.Manager()

    def show_domain_name(self):
        return self.domain_name