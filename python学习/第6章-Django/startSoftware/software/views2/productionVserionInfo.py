import logging
import time
from django.contrib import admin
from django.urls import path
from ..models import *

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko
from .. import views

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")



def manager_login(request):
    manager=ManagerForm()
    return render(request, 'software/restart_tomcat.html', locals())

def productionVserionInfo(request):
    

    return render(request, 'software/productionVserionInfo.html', locals())