import logging
import time
from django.contrib import admin
from django.urls import path

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko


# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")


@accept_websocket
def echo_once(request):
    print('这是一个好东西!')
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'software/echo_once.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
                command = 'sh /opt/test.sh'  # 这里是要执行的命令或者脚本

                # 远程连接服务器
                hostname = '192.168.43.100'
                username = 'root'
                password = '123456'

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                print('循环发送消息给前端页面!!')
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
                    print(nextline)
                    # 判断消息为空时,退出循环
                    if not nextline:
                        print('判断消息为空时,退出循环')
                        break

                print('关闭ssh连接')
                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))