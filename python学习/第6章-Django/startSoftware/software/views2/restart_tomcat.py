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


class ssh_linux(object):
    def __init__(self,hostname,username,password,port=22):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.port=port

    # 连接Linux服务器
    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password, timeout=60)
        self.ssh=ssh
        return self.ssh

    # 实例化一个transport对象执行shell命令
    def transport(self):
        '''
        基于SSHClient是传统的连接服务器、执行命令、关闭的一个操作，
        有时候需要登录上服务器执行多个操作，比如执行命令、上传/下载文件，
        上面方法则无法实现，可以通过如下方式来操作
        '''
        self.transport=paramiko.Transport(self.hostname,self.port)
        self.transport.connect(username=self.username,password=self.password)
        self.transport_ssh=paramiko.SSHClient()
        self.transport_ssh._transport=self.transport
        return self.transport

    # 连接linux服务器后直接执行shell命令
    def exec_command(self,command):
        stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)
        return stdin, stdout, stderr

    # 激活虚拟终端shell
    def client_shell(self):
        channel = self.ssh.invoke_shell()
        # print('设置读、写操作超时时间')
        channel.settimeout(60)
        time.sleep(0.5)
        self.channel=channel
        return self.channel

    # 连接虚拟终端执行shell命令
    def client_send_command(self,command):
        self.channel.send(command + '\n')
        time.sleep(0.5)
        try:
            command_res = self.channel.recv(65533).decode('utf-8')
            return command_res
        except Exception as e:
            return e


    def transport_color(self):
        self.transport.close()

    # 关闭连接Linux
    def close(self):
        self.ssh.close()
        return True


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

    server_config = views.getConfig('config\\software_config\\shar_server_config.ini')
    pafa5_serverIP = server_config.get_value('pafa5_serverIP', 'ip_list')
    pafa3_serverIP = server_config.get_value('pafa3_serverIP', 'ip_list')
    lotus_serverIP = server_config.get_value('lotus_serverIP', 'ip_list')

    pafa5_ip_list = pafa5_serverIP.strip().split(',')
    pafa3_ip_list = pafa3_serverIP.strip().split(',')
    lotus_ip_list = pafa3_serverIP.strip().split(',')
    print('pafa5_ip_list：', pafa5_ip_list)
    print('pafa3_ip_list：', pafa3_ip_list)
    print('lotus_ip_list：', lotus_ip_list)

    if not request.is_websocket():  # 判断是不是websocket连接
        print('如果是普通的http方法')
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            message=pafa5_ip_list
            return render(request, 'software/restart_tomcat.html', locals())
    else:
        for message in request.websocket:
            serverIP_list = message.decode('utf-8')  # 接收前端发来的数据
            print('serverIP_list: ',serverIP_list)

            command = 'sh /opt/test.sh'  # 这里是要执行的命令或者脚本
            # cmds=['export LANG=zh_CN.UTF-8','echo $LANG','pwd','dir -lh','hostname -i','date']
            cmds = ['tail -F /opt/test.log']

            # 远程连接服务器
            server_config = views.getConfig('config\\software_config\\shar_server_config.ini')
            hostname = server_config.get_value('serverIP', 'hostname')
            username = server_config.get_value('serverIP', 'username')
            password = server_config.get_value('serverIP', 'password')
            print('hostname,username,password: ', hostname, username, password)

            # 连接服务器并执行命令
            ssh=ssh_linux(hostname,username,password)
            ssh.connect()

            # 执行命令方法一，激活虚拟终端shell
            ssh.client_shell()
            command_res=ssh.client_send_command('ls -lh')
            print('command_res:  :',command_res)
            # ssh.close()

            # 执行命令方法二，直接执行命令
            stdin, stdout, stderr=ssh.exec_command('df -h')
            while True:
                nextline = stdout.readline().strip()
                print(nextline)
                time.sleep(0.5)
                if not nextline:
                    print('判断消息为空时,退出循环')
                    break
            # 关闭连接
            ssh.close()

            # ssh = paramiko.SSHClient()
            # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.connect(hostname=hostname, username=username, password=password, timeout=60)
            #
            # print('激活连接的终端！')
            # channel = ssh.invoke_shell()
            # print('设置读、写操作超时时间')
            # channel.settimeout(10)
            # time.sleep(0.5)

            # 根据不同服务器类型执行不同的shell脚本或shell命令
            for ip in serverIP_list:
                if ip in lotus_serverIP:
                    pass
                elif ip in pafa3_ip_list:
                    pass
                elif ip in pafa5_ip_list:
                    pass
                else:
                    pass

            # print('发送命令行：%s' % cmds)
            # for command in cmds:
            #     channel.send(command + '\n')
            #     time.sleep(0.5)
            #     try:
            #         command_res = channel.recv(65533).decode('utf-8')
            #         print('---' * 30)
            #         print(type(command_res))
            #         print(command_res)
            #         print('===' * 30)
            #         request.websocket.send(command_res.encode('utf-8'))  # 发送消息到客户端
            #     except Exception as e:
            #         print('***' * 30)
            #         print(e)
            #         continue
            #
            # channel.close()
            # ssh.close()


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
