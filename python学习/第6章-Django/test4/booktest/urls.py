#-*- coding:utf-8 -*-
#author:YJ沛


from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path('^htmltest$',views.htmltest,name='htmltest'),
    re_path('^(user1)$', views.user1, name='user1'),
    re_path('^(user)$', views.base2_user,name='base2_user'),
    path('', views.index,name='index'),
    re_path(r'^(\d+\S+)/(\d+)', views.show, name='show'),
    re_path('', views.index2,name='index2'),


]

