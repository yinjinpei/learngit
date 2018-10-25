#-*- coding:utf-8 -*-
#author:YJ沛

'''
select 原理
在多路复用的模型中，比较常用的有select模型和epoll模型。这两个都是系统接口，由操作系统提供。当然，Python的select模块进行了更高级的封装。

网络通信被Unix系统抽象为文件的读写，通常是一个设备，由设备驱动程序提供，驱动可以知道自身的数据是否可用。支持阻塞操作的设备驱动通常会实现
一组自身的等待队列，如读/写等待队列用于支持上层(用户层)所需的block或non-block操作。设备的文件的资源如果可用（可读或者可写）则会通知进程
，反之则会让进程睡眠，等到数据到来可用的时候，再唤醒进程。

这些设备的文件描述符被放在一个数组中，然后select调用的时候遍历这个数组，如果对于的文件描述符可读则会返回改文件描述符。当遍历结束之后，
如果仍然没有一个可用设备文件描述符，select让用户进程则会睡眠，直到等待资源可用的时候在唤醒，遍历之前那个监视的数组。
每次遍历都是依次进行判断的
'''

#跨平台,windows，linux等平台可以用

from socket import *
import select
import sys

server_socket = socket(AF_INET,SOCK_STREAM)
local_ip_and_port = ('', 7788)
server_socket.bind(local_ip_and_port)
server_socket.listen(10)

# 存放已连接上的客户端和服务器套接字
inputs = [server_socket]

#存放已连接上的新客户端信息
client_info_dect = {}


while True:
    # 调用select函数，阻塞等待
    readable, writeable, exceptional = select.select(inputs,[],[])
    # 括号中的三个参数意义：
        # 第一个参数：检测这个列表中的套接字是否可以收数据
        # 第二个参数：检测这个列表中的套按字可否发数据
        # 第三个参数：检测这个列表中的套接字是否产生了异常

    # 数据抵达，遍历读取
    for sock in readable:

        # 监听到有新的连接
        if sock == server_socket:
            client_socket, client_data = server_socket.accept()
            inputs.append(client_socket)
            client_info_dect[client_socket] = client_data
        else:
            revc_data = sock.recv(1024)
            if revc_data:
                print("%s: %s"%(client_info_dect[sock],revc_data))
                sock.send(revc_data)
            else:
                inputs.remove(sock)
                sock.close()