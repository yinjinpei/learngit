#-*- coding:utf-8 -*-
#author:YJ沛

import time

def application(env, start_response):
    status = "200 OK"
    headers = [("Content-Ty", "text/plain"), ("Connection", "keep-alive")]

    start_response(status, headers)
    return time.ctime()
