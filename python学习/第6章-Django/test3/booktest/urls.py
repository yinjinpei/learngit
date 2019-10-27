# coding:utf-8
# author:YJ沛


from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index),

]
