#-*- coding:utf-8 -*-
#author:YJ沛

from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    path('admin', admin.site.urls), # 访问管理页面
    re_path('addSoftware$', views.addSoftware, name='addSoftware'),
    re_path('delSoftware$', views.delSoftware, name='delSoftware'),
    re_path('uploadFile$', views.uploadFile, name='uploadFile'),
    re_path('downloadFile$', views.downloadFile, name='downloadFile'),
    re_path('delFile$', views.delFile, name='delFile'),
    path('', views.index,name='index'),
    # re_path('^WeChat$' ,views.WeChat,name='WeChat'),
    # re_path('^navicat$' ,views.navicat,name='navicat'),
    # re_path('^YoudaoNote$' ,views.YoudaoNote,name='YoudaoNote'),
    re_path('' ,views.openAppHelper,name='openAppHelper'),
]

