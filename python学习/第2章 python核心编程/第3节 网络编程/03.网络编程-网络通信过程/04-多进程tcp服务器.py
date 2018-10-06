#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *
from multiprocessing import Process



def responseClient(clientSocket,clientInfo):
    try:
        while True:
            # 等待接收客户端发来的数据
            recvClientData = clientSocket.recv(1024)

            # 当收到的数据为0时，表示客户端已断开连接，否则还在线中
            if len(recvClientData)>0:
                print('来自%s ：%s'%(clientInfo,recvClientData.decode('gb2312')))
                clientSocket.send('你好呀！'.encode('gb2312'))
            else:
                break

    except EOFError:
        pass
    # 关闭套接字
    clientSocket.close()

def main():
    # 创建套接字
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # 解决程序占用端口问题
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定IP和port
    serverSocket.bind(("", 5577))

    # 监听模式，连接数为100
    serverSocket.listen(100)

    connectSum = 0
    print('当前客户端连接数为：%s, 正在等待其他客户连接...' % connectSum)

    while True:
        # 等待接收客户端进行连接
        clientSocket, clientInfo = serverSocket.accept()

        connectSum += 1
        print('当前客户端连接数为：%s, 正在等待其他客户连接...'%connectSum)

        # 创建子进程，一对一响应客户
        P = Process(target=responseClient, args=(clientSocket,clientInfo))
        P.start()

        # 因为已经向子进程中copy了一份（引用），并且父进程中这个套接字也没有用处了,所有关闭
        clientSocket.close()

if __name__=="__main__":
    main()