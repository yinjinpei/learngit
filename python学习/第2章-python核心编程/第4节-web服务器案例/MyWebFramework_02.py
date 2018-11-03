# coding:utf-8
# author:YJ沛
# 07-web框架-my_web_framework.py
# 对应文件 MyWebFramework_02.py
# 添加静态文件处理，之前的是不分静或动态的

import time
from MyWebServer_02 import HttpServer


# 设置静态文件根目录
HTML_ROOT_DIR = "./static"


class Application(object):
    '''框架的核心部分， 也就是框架的主题程序，框架是通过的'''
    def __init__(self, urls):
        self.urls = urls
        print(self.urls)    # for test

    def __call__(self, env, start_response):

        # 查找env字典中有没有“PATH_INNFO”的值：file_name，如果没有默认设定为“/”
        path = env.get("PATH_INFO", "/")
        print("当前访问路径是: %s" % path)

        # 静态文件处理，一般静态文件都会存放在/static目录下
        if path.startswith("/static"):

            # 去除前面6位/static，匹配后面文件/index.html
            file_name = path[7:]
            try:
                file = open(HTML_ROOT_DIR + file_name, "rb")
            except IOError:
                status = "404 Not Found!"
                headers = []
                start_response(status, headers)
                return "The static file is not found!"
            else:
                file_data = file.read()
                print("当前访问内容是: %s" % file_data)

                file.close()

                status = "200 OK"
                headers = []
                start_response(status, headers)
                return file_data.decode("utf-8")


        #("/ctime", show_ctime)
        for url,handler in self.urls:
            if path == url:
                return handler(env, start_response)

        # 代表未找到路由信息，返回404错误
        status = "404 Not Found!"
        headers = []
        start_response(status, headers)
        return "not found!!"

# handler
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

def say_haha(env, start_response):
    status = "200 OK"
    headers = [
        ("Conntent-Type", "text/plain")
    ]
    start_response(status, headers)
    return "say_haha!!!!"

def index_html(env, start_response):
    status = "404 Not Found!"
    headers = []
    start_response(status, headers)
    return """
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>沛哥办公室</title>
        </head>
        <body>
        <h1> ----默认主页 http://127.0.0.1:8000----</h1>
        
        wellcome to 沛哥办公室！
        
        </body>
        </html>
    """


if __name__ == "__main__":

    urls = {
        ("/", index_html),
        ("/ctime", show_ctime),
        ("/sayhello", say_hello),
        ("/sayhaha", say_haha),

    }

    app = Application(urls)
    http_server = HttpServer(app)
    http_server.bind(8000)
    http_server.start()
