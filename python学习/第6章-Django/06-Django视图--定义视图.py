# coding:utf-8
# author:YJ沛

'''
定义视图
    1，本质就是一个函数
    2，视图的参数
        1)一个HttpRequest实例
        2)通过正则表达式组获取的位置参数
        3)通过正则表达式组获得的关键字参数
    3，在应用目录下默认有views.py文件，一般视图都定义在这个文件中
    4，如果处理功能过多，可以将函数定义到不同的py文件中
        新建views1.py
        #coding:utf-8
        from django.http import HttpResponse
        def index(request):
            return HttpResponse("你好")

        在urls.py中修改配置
        from . import views1
        url(r'^$', views1.index, name='index'),


错误视图
    Django原生自带几个默认视图用于处理HTTP错误


404 (page not found) 视图
    1，defaults.page_not_found(request, template_name='404.html')
    2，默认的404视图将传递一个变量给模板：request_path，它是导致错误的URL
    3，如果Django在检测URLconf中的每个正则表达式后没有找到匹配的内容也将调用404视图
    4，如果在settings中DEBUG设置为True，那么将永远不会调用404视图，而是显示URLconf 并带有一些调试信息

    5，在templates中创建404.html
        <!DOCTYPE html>
        <html>
        <head>
            <title></title>
        </head>
        <body>
        找不到了
        <hr/>
        {{request_path}}
        </body>
        </html>


    6，在settings.py中修改调试
        DEBUG = False
        ALLOWED_HOSTS = ['*', ]

    7，请求一个不存在的地址
        http://127.0.0.1:8000/test/


500 (server error) 视图
    1，defaults.server_error(request, template_name='500.html')
    2，在视图代码中出现运行时错误
    3，默认的500视图不会传递变量给500.html模板
    4，如果在settings中DEBUG设置为True，那么将永远不会调用505视图，而是显示URLconf 并带有一些调试信息


400 (bad request) 视图
    1，defaults.bad_request(request, template_name='400.html')
    2，错误来自客户端的操作
    3，当用户进行的操作在安全方面可疑的时候，例如篡改会话cookie

'''
