#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *

# 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

# 做准备接收方的地址
sendAddr = ('192,168,0.10', 8080)

# 输入发送内容
sendMsg = input('请输入要发送的数据：')

# 发送内容
udpSocker.sendto(sendMsg.encode(encoding='utf8'),sendAddr)

udpSocker.close()