# -*- coding:utf-8 -*-
#author:YJ沛

import socket
def application(env, start_response):
    status = "201 OK"
    headres = [("Content-Ty", "text/plain"), ("Connection", "keep-alive")]
    start_response(status, headres)

    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    # print(ip) # for test
    return "Server IP: %s" % ip

