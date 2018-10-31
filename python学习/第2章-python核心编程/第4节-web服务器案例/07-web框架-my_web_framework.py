# coding:utf-8
# author:YJ沛


import time

class Application(object):
    ''''''
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):

        # 查找env字典中有没有“Content-Type”，如果没有默认设定为“/”
        path = env.get("Content-Type", "/")
        for url,handler in urls:
            pass




app = Application()

def application(env, start_response):

    urls = {
        ("/ctime", show_ctime),
        ("/sayhello", say_hello),
    }

    status = "200 OK"

    headers = [
        ("Content-Type", "text/plain")
    ]

    start_response(status, headers)

    return time.ctime()