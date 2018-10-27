#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *
from threading import Thread


# 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

def recvData():
    # 设置地址和端口
    bindAddr = ('', 7788)   # ip地址和端口号，ip一般不填写，表示本机的任何一个
    # 绑定地址和端口
    udpSocker.bind(bindAddr)

    while True:
        # 等待接收内容
        recvMsg = udpSocker.recvfrom(1024)  # 1024表示本次接收的最大字节数
        # 显示接收内容
        print('\r收到内容: %s: %s '%(recvMsg[1],recvMsg[0].decode('gb2312')))
        print('\r请输入发送内容：',end='')


def sendData():
    # 设置接收方IP和端口
    sendAddr = ('192.168.0.100', 8080)

    while True:
        # 设置发送内容
        sendMsg = input("\r请输入发送内容：")
        # 发送消息
        udpSocker.sendto(sendMsg.encode('gb2312'), sendAddr)



if __name__ == "__main__":
    t = Thread(target=recvData)
    t2 = Thread(target=sendData)

    t.start()
    t2.start()

    t.join()
    t2.join()

    # 关闭套接字
    #udpSocker.close()