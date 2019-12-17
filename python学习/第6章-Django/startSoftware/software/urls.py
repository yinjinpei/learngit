#-*- coding:utf-8 -*-
#author:YJ沛


from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    # re_path('^WeChat$' ,views.WeChat,name='WeChat'),
    # re_path('^navicat$' ,views.navicat,name='navicat'),
    # re_path('^YoudaoNote$' ,views.YoudaoNote,name='YoudaoNote'),
    re_path('.*' ,views.openAppHelper,name='openAppHelper'),
]

