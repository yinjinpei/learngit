# coding:utf-8
# author:YJ沛
# 07-web框架-my_web_framework.py

import time
from MyWebServer import HttpServer

class Application(object):
    '''框架的核心部分， 也就是框架的主题程序，框架是通过的'''
    def __init__(self, urls):
        self.urls = urls
        print(self.urls)

    def __call__(self, env, start_response):

        # 查找env字典中有没有“PATH_INNFO”，如果没有默认设定为“/”
        path = env.get("PATH_INFO", "/")

        #("/ctime", show_ctime)
        for url,handler in self.urls:
            if path == url:
                return handler(env, start_response)

        # 代表未找到路由信息，返回404错误
        status = "404 Not Found!"
        headers = []
        start_response(status, headers)
        return "not found!!"


def show_ctime(env, start_response):
    status = "200 OK"
    headers = [
        ("Conntent-Type", "text/plain")
    ]
    start_response(status, headers)
    return time.ctime()

def say_hello(env, start_response):
    status = "200 OK"
    headers = [
        ("Conntent-Type", "text/plain")
    ]
    start_response(status, headers)
    return "say_hello!!!!"


if __name__ == "__main__":

    urls = {
        ("/", show_ctime),
        ("/ctime", show_ctime),
        ("/sayhello", say_hello),
    }

    app = Application(urls)
    http_server = HttpServer(app)
    http_server.bind(8000)
    http_server.start()
