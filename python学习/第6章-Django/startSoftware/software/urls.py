#-*- coding:utf-8 -*-
#author:YJ沛

from django.contrib import admin
from django.urls import path,re_path
from . import views
from .views2 import restart_tomcat


urlpatterns = [
    path('admin', admin.site.urls), # 访问管理页面
    re_path('^versionManagerIndex$', views.versionManagerIndex, name='versionManagerIndex'),
    re_path('^T8_index', views.T8_index, name='T8_index'),
    re_path('^CDNofflink', views.CDNofflink, name='CDNofflink'),
    re_path('addSoftware$', views.addSoftware, name='addSoftware'),
    re_path('delSoftware$', views.delSoftware, name='delSoftware'),
    re_path('uploadFile$', views.uploadFile, name='uploadFile'),
    re_path('downloadFile$', views.downloadFile, name='downloadFile'),
    re_path('delFile$', views.delFile, name='delFile'),
    re_path('setServerDate$', views.setServerDate, name='setServerDate'),
    re_path('delServerDate$', views.delServerDate, name='delServerDate'),
    re_path('productionMaterials', views.productionMaterials, name='productionMaterials'),
    re_path('tdc$', views.tdc, name='tdc'),
    re_path('newDirectory$', views.newDirectory, name='newDirectory'),
    re_path('rename_directory$', views.rename_directory, name='rename_directory'),
    re_path('allFileDownload$', views.allFileDownload, name='allFileDownload'),
    re_path('unblockedVersion$', views.unblockedVersion, name='unblockedVersion'),
    re_path('extranetAddress$', views.extranetAddress, name='extranetAddress'),
    re_path('loginSuperManager$', views.loginSuperManager, name='loginSuperManager'),
    re_path('logoutSuperManager$', views.logoutSuperManager, name='logoutSuperManager'),
    re_path('restart_tomcat$', restart_tomcat.restart_tomcat),
    # re_path('exec_command$', views.exec_command, name='exec_command'),
    # re_path('websocket_test$', views.websocket_test, name='websocket_test'),
    re_path('test$', views.test, name='test'),
    path('', views.index,name='index'),
    # re_path('^WeChat$' ,views.WeChat,name='WeChat'),
    # re_path('^navicat$' ,views.navicat,name='navicat'),
    # re_path('^YoudaoNote$' ,views.YoudaoNote,name='YoudaoNote'),
    re_path('' ,views.openAppHelper,name='openAppHelper'),
]

