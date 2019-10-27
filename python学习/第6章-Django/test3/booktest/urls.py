# coding:utf-8
# author:YJ沛


from django.urls import path,re_path
from . import views


urlpatterns = [
    path('',views.index),
    path('booktest',views.index2),  #只匹配'booktest'字符
    re_path('booktest',views.index3),   #匹配包含'booktest'字符

    # 如果不是re_path,而是使用的path则使用正则匹配带数字路径的时候语法都不会高亮，从而会导致404
    re_path('(\d+)',views.detail),
]
