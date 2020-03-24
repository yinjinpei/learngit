#-*- coding:utf-8 -*-

import os
import time
import datetime
import paramiko


# with open('ftp://peter@192.168.0.20/peter/123.py','+rb') as f:
#     pass

class TheServerHelper():
    """初始化函数构造
        其中remote有两个作用，除了字面的服务器路径外
        还作为执行的语句"""
    def __init__(self,serverIP,username,password,remote='',server_dir='',local_dir='',ftpType='',port=22):
        self.serverIP = serverIP
        self.username = username
        self.password = password
        self.port = port
        self.ftpType = ftpType
        self.remote = remote
        self.server_dir = server_dir
        self.local_dir = local_dir

    #SSH连接服务器，用于命令执行
    def ssh_connectionServer(self):
        try:
            # 创建SSH对象
            sf = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            sf.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            sf.connect(hostname=self.serverIP, port=self.port, username=self.username,
                                          password=self.password)
            set_time="date -s '20210320 12:00:00'"

            # 注意：依次执行多条命令时，命令之间用分号隔开
            stdin, stdout, stderr = sf.exec_command(self.remote+';'+"cd a"+';'+"sh a.sh"+';'+set_time)
            result = stdout.read().decode('utf-8')
            print("\033[36m%s\033[0m"%result)
        except:
            return False
        return True

    #FTP连接服务器，用于文件上传和下载
    def ftp_connectionServer(self):
        try:
            # 创建ftp对象
            sf = paramiko.Transport(self.serverIP, self.port)
            sf.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(sf)
        except:
            return False
        """定义参数ftpType：
                    ftpType=1    单个文件从其他服务器向本地下载
                    ftpType=2    单个文件向服务器上传
                    ftpType=3    文件夹下内容下载
                    ftpType=4    文件夹下内容上传"""
        local_path = os.path.dirname(self.local_dir)
        if self.ftpType=='1':
            if not os.path.exists(local_path):
                os.makedirs(local_path)
                sftp.get(self.server_dir,self.local_dir)
                sf.close()
                return True
        elif self.ftpType=='2':
            print('-------------------2222')
            print(self.local_dir, self.server_dir)
            sftp.put(self.local_dir,self.server_dir)
            print('-------------------33333333')
            sf.close()
            print('-------------------44444444444')
            return True
        else:
            print('-------------------5555555555555')
            return False


s1=TheServerHelper('192.168.0.200','root','123456','ls -lh',server_dir='/root/yinjinpei/123.py',
                   local_dir='G:\\123.py',ftpType='2')
s1.ssh_connectionServer()
s1.ftp_connectionServer()




