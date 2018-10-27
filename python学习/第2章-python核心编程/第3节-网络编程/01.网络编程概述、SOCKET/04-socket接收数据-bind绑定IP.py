#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *

#1 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

#2 设置地址和端口
bindAddr = ('', 7788)   # ip地址和端⼝号，ip⼀般不⽤写，表示本机的任何⼀一个

#3 绑定地址和端口
udpSocker.bind(bindAddr)


#4 等待接收内容
recvMsg = udpSocker.recvfrom(1024)  # 1024表示本次接收的最⼤字节数

#5 显示对⽅发送的数据
print(recvMsg)

# 关闭套接字
udpSocker.close()