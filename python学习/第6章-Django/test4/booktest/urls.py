#-*- coding:utf-8 -*-
#author:YJ沛


from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    re_path(r'^(\d+\S+)/(\d+)', views.show, name='show'),
    re_path('', views.index2,name='index2'),
]

