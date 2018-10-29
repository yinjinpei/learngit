#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *

# 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

# 准备接收方的地址
sendIP = input('请输入目的IP：')
sendPort = int(input('请输入目的端口号：'))

#设置发送内容
sendMsg = input('请输入要发送的内容：')

#发送
udpSocker.sendto(sendMsg.encode('utf-8'),(sendIP,sendPort))

# 接收内容
recvMsg = udpSocker.recvfrom(1024)  # 1024表示本次接收的最⼤字节数

# 显示对⽅发送的数据
print(recvMsg)

# 关闭套接字
udpSocker.close()