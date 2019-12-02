# coding:utf-8
# author:YJ沛

from django.urls import path,re_path
from . import views

urlpatterns=[
    re_path(r'^$',views.index)
]