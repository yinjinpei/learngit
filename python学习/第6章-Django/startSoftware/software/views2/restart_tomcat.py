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


@accept_websocket
def restart_tomcat(request):
    if not request.session.get('is_login', None):
        return render(request, 'software/index.html')

    manager = ManagerForm()
    setpassword = SetPasswordForm()

    if request.session.get('manager_islogin', None):
        print('manager_islogin值：',request.session.get('manager_islogin', None))
        manager_islogin = True
    else:
        # 如果用户的二级密码在数据库中有数据了就不是首次登录
        try:
            managers = ManagerDate.managers.get(user=request.session['user_name'])
            first_login = False
        except:
            first_login = True

        # 要求用户输入二级密码并处理，保存至cokie
        if request.method == "POST":
            manager_islogin = False
            try:
                managers = ManagerDate.managers.get(user=request.session['user_name'])
                manager_from = ManagerForm(request.POST)
                if manager_from.is_valid():
                    if managers.password == manager_from.cleaned_data['password']:
                        manager_islogin = True
                        request.session['manager_islogin'] = True
            except:
                # 首次登录时，要求用户设置二级密码并写入数据库中
                first_login = True
                setpassword_from = SetPasswordForm(request.POST)
                if setpassword_from.is_valid():
                    newManager = ManagerDate.managers.create()
                    newManager.user = request.session['user_name']
                    if setpassword_from.cleaned_data['password1'] == setpassword_from.cleaned_data['password2']:
                        newManager.password = setpassword_from.cleaned_data['password1']
                        newManager.save()
                        first_login = False

        return render(request, 'software/restart_tomcat.html', locals())

    print('这是一个好东西!')
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'software/restart_tomcat.html', locals())
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
                command = 'sh /opt/test.sh'  # 这里是要执行的命令或者脚本
                # cmds=['export LANG=zh_CN.UTF-8','echo $LANG','pwd','dir -lh','hostname -i','date']
                cmds=['w','date','sh /opt/test.sh']

                # 远程连接服务器
                server_config=views.getConfig('config\\software_config\\restart_tomcat.ini')
                hostname=server_config.get_value('shar_server_config','hostname')
                username=server_config.get_value('shar_server_config','username')
                password=server_config.get_value('shar_server_config','password')
                print('hostname,username,password: ',hostname,username,password)

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, username=username, password=password,timeout=60)

                # # 实例化一个transport对象
                # transport = paramiko.Transport(hostname, 22)
                # # 建立连接
                # transport.connect(username=username, password=password)
                # # 将sshclient的对象的transport指定为以上的transport
                # ssh = paramiko.SSHClient()
                # ssh._transport = transport
                # for command in cmds:
                #     # 执行命令，和传统方法一样
                #     stdin, stdout, stderr = ssh.exec_command('cd /opt;./test.sh')
                #     # print(stdout.read().decode())
                #     while True:
                #         nextline = stdout.readline().strip() # 读取脚本输出内容
                #         request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
                #         print(nextline)
                #         # 判断消息为空时,退出循环
                #         if not nextline:
                #             print('判断消息为空时,退出循环')
                #             break
                # # 关闭连接
                # transport.close()
                # ssh.close()


                print('激活连接的终端！')
                channel = ssh.invoke_shell()
                print('设置读、写操作超时时间')
                channel.settimeout(10)
                time.sleep(0.5)

                print('发送命令行：%s' % cmds)
                for command in cmds:
                    channel.send(command + '\n')
                    time.sleep(0.5)
                    try:
                        command_res = channel.recv(65533).decode('utf-8')
                        print('--' * 30)
                        print(type(command_res))
                        print(command_res)
                        print('==' * 30)
                        while True:
                            nextline = command_res.readline().strip()  # 读取脚本输出内容
                            request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
                            print(nextline)
                            # 判断消息为空时,退出循环
                            if not nextline:
                                print('判断消息为空时,退出循环')
                                break
                        request.websocket.send(command_res.encode('utf-8'))  # 发送消息到客户端
                    except Exception as e:
                        print('*' * 30)
                        print(e)
                        continue

                channel.close()
                ssh.close()

            #     # 务必要加上get_pty=True,否则执行命令会没有权限
            #     stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
            #     # result = stdout.read()
            #     print('stdin:',stdin)
            #     print('stdout:',stdout)
            #     print('stderr:',stderr)
            #
            #     # 循环发送消息给前端页面
            #     print('循环发送消息给前端页面!!')
            #     while True:
                #         nextline = stdout.readline().strip()  # 读取脚本输出内容
            #         request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
            #         print(nextline)
            #         # 判断消息为空时,退出循环
            #         if not nextline:
            #             print('判断消息为空时,退出循环')
            #             break
            #     ssh.close()  # 关闭ssh连接
            #     print('关闭ssh连接')
            # else:
            #     request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))


def manager_login(request):
    manager=ManagerForm()
    return render(request, 'software/restart_tomcat.html', locals())
