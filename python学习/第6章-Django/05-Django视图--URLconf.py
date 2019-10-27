# coding:utf-8
# author:YJ沛

'''
视图:
    视图接受Web请求并且返回Web响应
    视图就是一个python函数，被定义在views.py中
    响应可以是一张网页的HTML内容，一个重定向，一个404错误等等
    响应处理过程如下图：

    用户输入网址：-->项目根目录下manager.py中找(os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test3.settings')),这里指向(test3.settings)-->
    然后到test3.settings找（path('admin/', admin.site.urls)），这里指向'admin/'-->
    再然后到这里匹配admin，在admin.site.urls找

'''
