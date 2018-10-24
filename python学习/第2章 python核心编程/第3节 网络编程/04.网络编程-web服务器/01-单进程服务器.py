#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *

#1，创建网编套接字
server_socket = socket(AF_INET, SOCK_STREAM)

#2，绑定本地IP和port
local_ip_and_port = ("",7878)

#3，将套接字变成监听（被动）
server_socket.listen(1024)

client_socket = []

while True:
    print("----等待接收数据----")

    #4，等待接收
    new_socket, dest_data = server_socket.accept()
    client_socket.append(new_socket)

    if dest_data:
        print(dest_data)
    else:
        pass