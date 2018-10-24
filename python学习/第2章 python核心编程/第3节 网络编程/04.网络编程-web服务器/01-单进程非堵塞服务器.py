#-*- coding:utf-8 -*-
#author:YJ沛
#单进程非堵塞服务器

from socket import *

# 1，创建网编套接字
server_socket = socket(AF_INET, SOCK_STREAM)

# 2，绑定本地IP和port
local_ip_and_port = ("",7878)
server_socket.bind(local_ip_and_port)

# 3，以后这个socket变为非堵塞
server_socket.setblocking(False)

# 4，将套接字变成监听（被动）
server_socket.listen(100)

# 用来保存所有已连接成功的新客户端的信息
client_list = []

while True:


    try:
        # 5，等待一个新的客户端的到来（即完成三次握手的客户端）
        client_socket, client_data = server_socket.accept()

    except:
        pass
    else:
        print("----有新的客户来了----%s"%str(client_data))
        client_socket.setblocking(False)
        # 新的客户端socket添加到列表中
        client_list.append((client_socket,client_data))


    # 遍历列表
    for client_socket, client_data in client_list:
        try:
            # 接收客户端数据
            recvData = client_socket.recv(1024)
        except:
            # 如果没有客户端数据则不处理，跳过，继续往下执行
            pass
        else:
            # 如果进来的数据不是空值
            if recvData:
                print("%s: %s"%(str(client_data),recvData))
            else:
                # 收到的数据是空值，则关闭socket
                client_socket.close()
                client_list.remove((client_socket,client_data))
                print("%s：客户端已断开！！"%str(client_data))
