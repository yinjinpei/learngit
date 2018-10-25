#-*- coding:utf-8 -*-
#author:YJ沛

import sys
import time
import gevent

from gevent import socket,monkey

# 对下面代码都做动态处理
monkey.patch_all()

def handle_request(cilent_socket,client_data):
    while True:
        data = cilent_socket.recv(1024)
        if data:
            print("有数据到，%s: %s"%(str(client_data),data))
            cilent_socket.send(data)
        else:
            cilent_socket.close()
            break


def server(port):
    server_socket = socket.socket()
    local_ip_and_port = ("", 7788)
    server_socket.bind(local_ip_and_port)
    server_socket.listen(100)

    while True:
        client_socket, client_data = server_socket.accept()
        print(socket)
        print(client_data)
        gevent.spawn(handle_request,client_socket,client_data)


if __name__ == "__main__":
    server(7788)