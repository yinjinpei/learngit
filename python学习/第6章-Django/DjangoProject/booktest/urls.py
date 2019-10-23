# coding:utf-8
# author:YJ沛

from django.conf.urls import url
from . import views


urlpatterns=[
    url('^$',views.index)
]
