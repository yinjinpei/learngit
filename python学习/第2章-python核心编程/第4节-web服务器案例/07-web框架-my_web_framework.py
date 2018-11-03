# coding:utf-8
# author:YJ沛
# 参与MyWebFramework.py  MyWebServer.py

import time

class Application(object):
    ''''''
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):

        # 查找env字典中有没有“Content-Type”，如果没有默认设定为“/”
        path = env.get("Content-Type", "/")
        for url,handler in self.urls:
            pass




