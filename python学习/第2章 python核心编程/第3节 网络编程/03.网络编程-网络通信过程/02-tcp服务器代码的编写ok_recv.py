#-*- coding:utf-8 -*-
#author:YJ沛

"""
tcp特点：1，稳定  2，相对于udp而言要慢一些  3，web服器都是使用tcp开发
upd特点：1，不稳定  2，适当比tcp要快一些


创建tcp服务器流程：
1，socket创建一个套按字
2，bind绑定ip和port
3，listen使套接字变为可以被动链接
4，accept等待客端的链接
5，recv/send接收发送数据
6，关闭套接字

"""

from socket import *

# 创建套接字
serverSocket = socket(AF_INET,SOCK_STREAM)

# 绑定IP和端口，这里的IP表示本机的任何⼀一个
serverSocket.bind(("", 7788))

# 设置listen使套接字变为可以被动链接
serverSocket.listen(5)

# accept等待客端的链接
clientSocket, clientInfo = serverSocket.accept()

# recv/send接收发送数据
recvData = clientSocket.recv(1024)

# 关闭套接字
clientSocket.close()
serverSocket.close()