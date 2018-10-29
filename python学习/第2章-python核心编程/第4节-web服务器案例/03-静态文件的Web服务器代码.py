# -*- coding:utf-8 -*-
# author:YJ沛

import re
from socket import *
from multiprocessing import Process


# 设置静态文件根目录
HTML_ROOT_DIR = "./03-html"


def handle_client(client_socket, client_data):
    '''处理客户端请求'''

    # 获取客户端IP和端口
    client_ip, client_port = client_data
    try:
        while True:
            # 获取客户端请求数据
            recv_data = client_socket.recv(1024)

            # 解析请求报文
            if recv_data:

                # print("来自%s：\n%s" % (client_data, recv_data.decode('gb2312')))
                print("来自%s：\n%s" % (client_data, recv_data.decode('utf-8')))
                request_lines = recv_data.splitlines()

                for line in request_lines:
                    print(line)
                request_start_line = request_lines[0]

                # 提取用户请求的文件名
                file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode('utf-8')).group(1)
                print(file_name)    # for test  "/"

                try:
                    # 判断用户请求文件的路径是否为"/",并打开文件
                    if "/" == file_name:
                        read_file = open(HTML_ROOT_DIR + file_name + "index.html", "rb")
                        print(read_file)    # for test
                    else:
                        read_file = open(HTML_ROOT_DIR + file_name + "/index.html", "rb")
                        print(read_file)    # for test
                except IOError:
                    # 构造响应数据
                    response_start_line = "HTTP/1.1 404 Not Found!\r\n"
                    response_headers = "Server: My Server\r\n"
                    response_body = "The file is not found!!"
                    response = response_start_line + response_headers + "\r\n" + "<!DOCTYPE html>" + response_body
                    print(response)     # for tes

                    client_socket.send(bytes(response, "utf-8"))
                else:
                    # 获取客户请求文件内容
                    file_data = read_file.read()
                    read_file.close()
                    print(file_data)    # for test

                    # 构造响应数据
                    response_start_line = "HTTP/1.1 200 OK\r\n"
                    response_headers = "Server: My Server\r\n"
                    response_body = file_data.decode("utf-8")
                    response = response_start_line + response_headers + "\r\n" + response_body
                    print(response)  # for test

                    # client_socket.send(response.encode('gb2312'))
                    client_socket.send(bytes(response, "utf-8"))
            else:
                break

    except EOFError:
        pass
    # 关闭套接字
    print("%s:%s 已断开连接！！" % (client_ip, client_port))
    client_socket.close()


def main():
    # 1，创建server_socket
    server_socket = socket(AF_INET, SOCK_STREAM)

    # 解决程序占用端口问题（服务器先结束则会出现端口被占用）
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    local_ip_and_port = ("", 8000)
    server_socket.bind(local_ip_and_port)
    server_socket.listen(100)

    # 2,连接客户端
    while True:
        client_socket, client_data = server_socket.accept()

        # print("一个客户端已连接上：%s" % str(client_data))
        print("一个客户端已连接上：%s:%s" % client_data)

        # 创建子进程处理客户端的请求
        handle_client_process = Process(target=handle_client, args=(client_socket, client_data))
        handle_client_process.start()

        # 因为已经向子进程中copy了一份（引用），并且父进程中这个套接字也没有用处了,所有关闭
        client_socket.close()


if __name__ == "__main__":
    main()
