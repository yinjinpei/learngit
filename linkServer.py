# coding:utf-8
# SSH远程连接堡垒机操作系统，并选择目标主机资源id，进入目标主机执行批量命令

import time
import paramiko

def sshHost_sendCmd(ip,username,password,hosttype,port,cmds):
    ''' :param ip: 堡垒机ip
        :param username: 堡垒机用户
        :param password: 用户的密码
        :param hosttype: 主机类型，普通主机-normal，数据库主机-db
        :param port: 堡垒机端口
        :param cmds: 存放n个命令的列表
        :return:
    '''
    paramiko.util.log_to_file("paramiko.log")
    try: # excmd = ';'.join(cmds)
        s = paramiko.SSHClient() s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=ip, port=port, username=username, password=password)
        #激活连接的终端
        channel = s.invoke_shell()
        #读、写操作超时时间，10秒
        channel.settimeout(10)
        choose =''
        if hosttype == 'normal':
            choose = '0'+'\n'
            print(u'选择普通linux资源主机：0' )
        elif hosttype == 'db':
            choose = '1'+'\n'
            print(u'选择mysql资源主机：1')
        else:
            print(u'hosttype输入错误！（normal/db）' )
            #输入选择的资源主机
        channel.send(choose)
        #等待堡垒机连接资源主机成功
        time.sleep(5)
        #发送cmds中的指令到资源主机 for command in cmds: print u'执行命令：%s'%command
        channel.send(command+'\n')
        time.sleep(2)
        try:
            command_res = channel.recv(65533).decode('utf-8').strip()
            print(command_res)
        except Exception as e:
            print (u'在目标机(IP: %s)上进行读取操作超时')
            # break
        channel.close()
    except Exception as e:
        print(e)