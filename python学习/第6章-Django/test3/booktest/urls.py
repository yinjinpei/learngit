# coding:utf-8
# author:YJ沛


from django.urls import path,re_path
from . import views


urlpatterns = [
    path('',views.index),
    path('booktest',views.index2),  #只匹配'booktest'字符
    re_path('booktest',views.index3),   #匹配包含'booktest'字符

    # 如果不是re_path,而是使用的path则使用正则匹配带数字路径的时候语法都不会高亮，从而会导致404
    # re_path('(\d+)',views.detail),

    re_path(r'^(\d+)/(\d+)/(\d+)/$',views.detail2),  #匹配 数字/数字/数字/ ，如:2019/10/27

    # re_path('(?P<p1>\d+)/(?P<p2>\d+)/(?P<p3>\d+)/',views.detail3), #关键字参数，指定参数位置，和上面一样

    re_path(r'^peter',views.peter),


    re_path(r'^getTest1/$',views.getTest1),

    re_path(r'^getTest2/$',views.getTest2),

    re_path(r'^getTest3/$',views.getTest3),

]