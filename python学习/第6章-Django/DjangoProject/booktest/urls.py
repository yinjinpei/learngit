# coding:utf-8
# author:YJ沛

# from django.conf.urls import
from django.urls import path
from . import views


urlpatterns=[
    path('',views.index, name='index'),

]
