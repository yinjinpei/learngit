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

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(('192.168.0.7',8989))

clientSocket.send("haha_hehe".encode('gb2312'))

recvData = clientSocket.recv(1024)

print(recvData.decode('gb2312'))

clientSocket.close()