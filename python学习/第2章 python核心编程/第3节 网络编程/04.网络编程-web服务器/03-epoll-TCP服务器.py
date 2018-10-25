#-*- coding:utf-8 -*-
#author:YJ沛


'''大体框架
1，创建监听套按字
2，通过某些方式来检测哪些套按字可以进行收发数据了
3，对上面检测出来的套接字进行收发数据的处理

注意：需要在Linux上运行
'''

from socket import *
import select

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

local_ip_and_port = ("", 7788)
server_socket.bind(local_ip_and_port)
server_socket.listen(100)

# 创建一个epoll对象
epoll = select.epoll()

# 注册
epoll.register(server_socket.fileno(), select.EPOLLIN|select.EPOLLET)

connections = {}
addresses = {}

# 循环等待客户端的到来或者对方发送数据
while True:

    # epoll进行fd扫描的地方----未指定超时时间则为阻塞等待
    epoll_list = epoll.poll()

    # 对事件进行判断
    for fd,events in epoll_list:

        # 如果是socket创建的套接字则被激活
        if fd == server_socket.fileno():

            client_socket, clinet_data = server_socket.accept()
            print("有新的客户端连接上了：%s"%str(clinet_data))

            # 将新的客户端信息保存起来
            connections[client_socket.fileno()] = client_socket
            addresses[client_socket.fileno()] = clinet_data

            # 向epoll中注册连接socket的可读事件
            epoll.register(client_socket.fileno(), select.EPOLLIN|select.EPOLLET)

        elif events == select.EPOLLIN:

            # 从激活fd上接收
            recv_data = connections[fd].recv(1024)

            if recv_data:
                print("recv: %s: %s"%(str(addresses[fd]), recv_data))