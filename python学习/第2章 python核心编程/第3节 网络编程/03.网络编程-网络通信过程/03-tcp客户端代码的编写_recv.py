#-*- coding:utf-8 -*-
#author:YJ沛

'''
创建tcp客户端流程：
1，socket创建一个套接字
2，econnect连接服务器
3，send发送数据
4，recv接收数据
5，close关闭套接字

'''

from socket import *

#1，socket创建一个套接字
clientSocket = socket(AF_INET, SOCK_STREAM)

#2，econnect连接服务器
clientSocket.connect(('192.168.0.7',8989))

#3，send发送数据
clientSocket.send("haha_hehe".encode('gb2312'))

#4，recv接收数据
recvData = clientSocket.recv(1024)

print(recvData.decode('gb2312'))

#5，close关闭套接字
clientSocket.close()