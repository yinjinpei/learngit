#-*- coding:utf-8 -*-
#author:YJ沛


from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path('^captchaCode2$', views.captchaCode2),
    re_path('^captchaCode1$', views.captchaCode1),
    re_path('^captchaCode$', views.captchaCode),
    re_path('^gvcode2$', views.gvcode2),
    re_path('^gvcode$', views.gvcode),
    re_path('^verifyTest2$', views.verifyTest2),
    re_path('^verifyTest1$', views.verifyTest1),
    re_path('^verifyCode$',views.verifyCode),
    re_path('^csrf1$',views.csrf1),
    re_path('^csrf2$',views.csrf2),
    re_path('^htmltest$',views.htmltest,name='htmltest'),
    re_path('^(user1)$', views.user1, name='user1'),
    re_path('^(user)$', views.base2_user,name='base2_user'),
    path('', views.index,name='index'),
    re_path(r'^(\d+\S+)/(\d+)', views.show, name='show'),
    re_path('', views.index2,name='index2'),

]

