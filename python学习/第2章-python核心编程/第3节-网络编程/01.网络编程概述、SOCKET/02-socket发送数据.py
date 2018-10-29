#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *

# 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

# 做准备接收方的地址
sendIP = input("请输入接收人的IP地址：")
sendPort = int(input("请输入接收人的端口号："))
# 输入发送内容
sendMsg = input('请输入要发送的数据：')

# 发送内容
udpSocker.sendto(sendMsg.encode('utf-8'),(sendIP,sendPort))

#udpSocker.sendto(sendMsg.encode(encoding='gb2312'),sendAddr)

udpSocker.close()