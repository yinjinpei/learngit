#-*- coding:utf-8 -*-
#author:YJ沛


from socket import *
from multiprocessing import Process



def response_client(client_socket, client_data):
    try:
        while True:
            recv_Data = client_socket.recv(1024)
            if recv_Data:
                print("来自%s：\n%s"%(client_data,recv_Data.decode('gb2312')))


                client_socket.send("你好！！".encode('gb2312'))
            else:
                break

    except EOFError:
        pass

    # 关闭套接字
    client_socket.close()


def main():
    # 1，创建server_socket
    server_socket = socket(AF_INET,SOCK_STREAM)

    # 解决程序占用端口问题（服务器先结束则会出现端口被占用）
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    local_ip_and_port = ("",7788)
    server_socket.bind(local_ip_and_port)
    server_socket.listen(100)

    # 2,连接客户端
    while True:
        client_socket, client_data = server_socket.accept()
        P = Process(target=response_client, args=(client_socket, client_data))
        P.start()

        # 因为已经向子进程中copy了一份（引用），并且父进程中这个套接字也没有用处了,所有关闭
        client_socket.close()

if __name__=="__main__":
    main()