#-*- coding:utf-8 -*-
#author:YJ沛


from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    re_path(r'^(\d+\S+)', views.show, name='show')
]

