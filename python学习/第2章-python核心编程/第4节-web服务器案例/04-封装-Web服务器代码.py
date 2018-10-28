# -*- coding:utf-8 -*-
# author:YJ沛

import re
from socket import *
from multiprocessing import Process


# 设置静态文件根目录
HTML_ROOT_DIR = "./03-html"


class HttpServer():
    '''定义一个HttpServer服务器'''

    def __init__(self, port):
        '''初始化服务器'''
        # 1，创建server_socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # 解决程序占用端口问题（服务器先结束则会出现端口被占用）
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))

    def start_listen(self):
        '''把服务器变成被动，开始监听'''
        self.server_socket.listen(100)

    def start_accept(self):
        '''等待客户端的到来'''
        client_info = self.server_socket.accept()
        return client_info


class Handle_client():
    '''处理客户端请求'''

    def __init__(self, client_socket, client_data):
        self.client_ip, self.client_port = client_data
        self.client_socket = client_socket

    def retrieve_data(self):
        '''获取客户端请求数据'''
        self.recv_data = self.client_socket.recv(1024)
        return self.recv_data

    def analytical_data(self):
        '''解析请求报文,提取用户请求的文件名'''
        self.__request_lines = self.recv_data.splitlines()
        self.__request_start_line = self.__request_lines[0]
        self.file_name = re.match(
            r"\w+ +(/[^ ]*) ",
            self.__request_start_line.decode('utf-8')).group(1)
        return self.file_name

    def read_local_file(self):
        '''获取用户请求的本地文件内容'''
        if "/" == self.file_name:
            self.file_name = "/index.html"
        try:
            self.read_file = open(HTML_ROOT_DIR + self.file_name, "rb")
        except IOError:
            # 构造响应数据
            self.__response_start_line = "HTTP/1.1 404 Not Found!\r\n"
            self.__response_headers = "Server: My Server\r\n"
            self.__response_body = "The file is not found!!"
            self.response = self.__response_start_line + self.__response_headers + \
                "\r\n" + "<!DOCTYPE html>" + self.__response_body
        else:
            # 获取客户请求文件内容
            self.file_data = self.read_file.read()
            self.read_file.close()
            print(self.file_data)  # for test

            # 构造响应数据
            self.__response_start_line = "HTTP/1.1 200 OK\r\n"
            self.__response_headers = "Server: My Server\r\n"
            self.__response_body = self.file_data.decode("utf-8")
            self.response = self.__response_start_line + \
                self.__response_headers + "\r\n" + self.__response_body
        finally:
            return self.response

    def response_cilent(self):
        self.client_socket.send(bytes(self.response, "utf-8"))


def handle_client(client_socket, client_data):
    '''处理客户端请求'''

    handle_client_procesee = Handle_client(client_socket, client_data)

    try:
        while True:
            # 获取客户端请求数据
            recv_data = handle_client_procesee.retrieve_data()
            print('-' * 100)
            print(recv_data)    # for test
            print('-' * 100)
            # 解析请求报文
            if recv_data:
                print('=' * 100)
                print("来自%s：\n%s" % (client_data, recv_data.decode('utf-8')))
                print('=' * 100)

                # 提取用户请求的文件名
                file_name = handle_client_procesee.analytical_data()
                print("用户请求的文件名: %s" % file_name)    # for test  "/"

                response = handle_client_procesee.read_local_file()
                print("回复用户内容：%s " % response)  # for tes

                # 响应客户端
                client_socket.send(bytes(response, "utf-8"))
            else:
                break

    except EOFError:
        pass
    # 关闭套接字
    print(
        "%s:%s 已断开连接！！" %
        (handle_client_procesee.client_ip,
         handle_client_procesee.client_port))
    client_socket.close()


def main():
    http_server = HttpServer(8000)
    http_server.start_listen()

    # 2,连接客户端
    while True:
        client_socket, client_data = http_server.start_accept()

        # print("一个客户端已连接上：%s" % str(client_data))
        print("一个客户端已连接上：%s:%s" % client_data)

        # 创建子进程处理客户端的请求
        handle_client_process = Process(
            target=handle_client, args=(
                client_socket, client_data))
        handle_client_process.start()

        # 因为已经向子进程中copy了一份（引用），并且父进程中这个套接字也没有用处了,所有关闭
        client_socket.close()


if __name__ == "__main__":
    main()
