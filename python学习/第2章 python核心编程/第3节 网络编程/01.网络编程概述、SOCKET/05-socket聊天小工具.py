#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *
from threading import Thread
import time

# 创建一个套接字
udpSocker = socket(AF_INET, SOCK_DGRAM)

def recvData():
    # 设置地址和端口
    bindAddr = ('', 7788)   # ip地址和端⼝号，ip⼀般不⽤写，表示本机的任何⼀一个

    # 绑定地址和端口
    udpSocker.bind(bindAddr)

    while True:
        # 等待接收内容
        recvMsg = udpSocker.recvfrom(1024)  # 1024表示本次接收的最⼤字节数

        # 显示对⽅发送的数据
        print('收到内容：\n',recvMsg[0].decode('gb2312'))

        time.sleep(0.5)


def sendData():
    # 设置接收方IP和端口
    sendAddr = ('192.168.0.10', 8080)

    while True:
        # 设置发送内容
        sendMsg = input("\n请输入发送内容：")

        # 发送
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