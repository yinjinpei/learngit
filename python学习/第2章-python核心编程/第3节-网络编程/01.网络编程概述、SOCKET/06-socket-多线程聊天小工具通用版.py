# -*- coding:utf-8 -*-
# author:YJ沛

from socket import *
from threading import Thread

def recvData():
    # 设置地址和端口
    bindAddr = ('', sourcePort)  # ip地址和端口号，ip一般不填写，表示本机的任何一个
    # 绑定地址和端口
    udpSocker.bind(bindAddr)

    while True:
        # 等待接收内容
        recvMsg = udpSocker.recvfrom(1024)  # 1024表示本次接收的最大字节数
        # 显示接收内容
        print('\r收到内容: %s: %s ' % (recvMsg[1], recvMsg[0].decode('gb2312')))
        print('\r请输入发送内容：', end='')


def sendData():
    # 设置接收方IP和端口
    sendAddr = (targetIP, targetPort)

    while True:
        # 设置发送内容
        sendMsg = input("\r请输入发送内容：")
        # 发送消息
        udpSocker.sendto(sendMsg.encode('gb2312'), sendAddr)

def get_local_IP():
    hostname = gethostname()
    # 获取本机ip
    ip = gethostbyname(hostname)
    print('本机IP:',ip)

udpSocker = None
targetIP = ""
targetPort = 0
sourcePort = 0

def main():

    global udpSocker
    global targetIP
    global targetPort
    global sourcePort

    # 获取本机ip，并打印
    get_local_IP()

    # 创建一个套接字
    udpSocker = socket(AF_INET, SOCK_DGRAM)
    targetIP = input("请输入对方IP：")
    targetPort = int(input("请输入对方端口号："))
    sourcePort = int(input("请输入自己端口号："))

    t = Thread(target=recvData)
    t2 = Thread(target=sendData)

    t.start()
    t2.start()

    t.join()
    t2.join()

    # 关闭套接字
    # udpSocker.close()

if __name__ == "__main__":
    main()