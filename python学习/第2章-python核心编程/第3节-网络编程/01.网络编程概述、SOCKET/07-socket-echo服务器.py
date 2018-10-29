#-*- coding:utf-8 -*-
#author:YJ沛

'''
echo服务器：收集信息原路返回信息
'''

from socket import *

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

        # echo服务器重点，收到信息回应
        udpSocker.sendto(recvMsg[0],recvMsg[1])


def main():
    recvData()

    # 关闭套接字
    #udpSocker.close()

if __name__ == "__main__":
    main()


