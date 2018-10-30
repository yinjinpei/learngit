# -*- coding:utf-8 -*-
# author:YJ沛

import re
from socket import *
from multiprocessing import Process
import sys


# 设置静态文件根目录
HTML_ROOT_DIR = "./03-html"

# 添加搜索路径
WSGI_PATH = "./06-WSGI"

class HttpServer():
    '''定义http服务器'''
    def __init__(self):
        # 1，创建server_socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # 解决程序占用端口问题（服务器先结束则会出现端口被占用）
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self, port):
        local_ip_and_port = ("", port)
        self.server_socket.bind(local_ip_and_port)

    def start(self):
        '''等待连接客户端'''
        self.server_socket.listen(100)

        while True:
            client_socket, client_data = self.server_socket.accept()
            # 创建子进程处理客户端的请求
            self.handle_client_process = Process(target=self.handle_client, args=(client_socket, client_data))
            self.handle_client_process.start()
            # print("一个客户端已连接上：%s" % str(client_data))
            print("一个客户端已连接上：%s:%s" % client_data)

            # 因为已经向子进程中copy了一份（引用），并且父进程中这个套接字也没有用处了,所有关闭
            client_socket.close()

    def start_response(self, status, headers):
        '''获取动态加载的内容：
         status = "200 OK"
        headers = [
            ("Content-Ty", "text/plain"),
            ("Connection", "keep-alive")
        ]
        '''
        response_headers = "HTTP1.1 " + status + "\r\n"
        for header in headers:
            response_headers += "%s: %s\r\n" % header
            print(response_headers)     #for test
        # 赋予值给对象
        self.response_headers = response_headers

    def handle_client(self, client_socket, client_data):
        '''处理客户端请求'''

        # 获取客户端IP和端口
        client_ip, client_port = client_data
        try:
            while True:
                # 获取客户端请求数据
                recv_data = client_socket.recv(1024)

                # 解析请求报文
                if recv_data:

                    print("来自%s：\n%s" % (client_data, recv_data.decode('utf-8')))
                    # 解析请求报文
                    # 'GET / HTTP/1.1'
                    request_lines = recv_data.splitlines()
                    for line in request_lines:
                        print(line)
                    request_start_line = request_lines[0]

                    # 提取用户请求的文件名
                    file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode('utf-8')).group(1)
                    print(file_name)  # for test  "/"

                    # 解析客户的请求方式：GET
                    method = re.match(r"(\w+) +/[^ ]* ", request_start_line.decode('utf-8')).group(1)
                    print(method)

                    if file_name.endswith(".py"):
                        try:
                            ctime = __import__(file_name[1:-3])
                        except Exception:
                            self.response_headers = "HTTP/1.1 404 Not Found\r\n"
                            response_body = "The file is not found!"
                        else:
                            # 拿到客户端请求的信息
                            env = {"PATH_INFO": file_name, "METHOD": method}
                            response_body = ctime.application(env, self.start_response)

                        response = self.response_headers + "\r\n" + "<!DOCTYPE html>" + response_body
                        # client_socket.send(bytes(response, "utf-8"))
                    else:
                        try:
                            # 判断用户请求文件的路径是否为"/",并打开文件
                            if "/" == file_name:
                                read_file = open(HTML_ROOT_DIR + file_name + "index.html", "rb")
                                print(read_file)  # for test
                            else:
                                read_file = open(HTML_ROOT_DIR + file_name + "/index.html", "rb")
                                print(read_file)  # for test
                        except IOError:
                            # 构造响应数据
                            response_start_line = "HTTP/1.1 404 Not Found!\r\n"
                            response_headers = "Server: My Server\r\n"
                            response_body = "The file is not found!!\r\n"
                            response = response_start_line + response_headers + "\r\n" + "<!DOCTYPE html>" + response_body
                            print(response)  # for tes

                            # client_socket.send(bytes(response, "utf-8"))
                        else:
                            # 获取客户请求文件内容
                            file_data = read_file.read()
                            read_file.close()
                            print(file_data)  # for test

                            # 构造响应数据
                            response_start_line = "HTTP/1.1 200 OK\r\n"
                            response_headers = "Server: My Server\r\n"
                            response_body = file_data.decode("utf-8")
                            response = response_start_line + response_headers + "\r\n" + response_body
                            print(response)  # for test

                            # client_socket.send(bytes(response, "utf-8"))

                    # 响应客户的请求
                    client_socket.send(bytes(response, "utf-8"))
                else:
                    break

        except EOFError:
            pass
        # 关闭套接字
        print("%s:%s 已断开连接！！" % (client_ip, client_port))
        client_socket.close()



def main():
    # 添加搜索路径
    sys.path.insert(1, WSGI_PATH)
    http_server = HttpServer()
    http_server.bind(8000)
    http_server.start()

if __name__ == "__main__":
    main()
