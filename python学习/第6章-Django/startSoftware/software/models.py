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
    FileName = forms.CharField(label="输入文件名可直接删除，请输入文件名", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))


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

