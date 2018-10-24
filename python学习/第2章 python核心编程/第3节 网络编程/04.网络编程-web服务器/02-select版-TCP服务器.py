#-*- coding:utf-8 -*-
#author:YJ沛

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