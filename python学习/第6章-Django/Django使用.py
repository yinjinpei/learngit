# coding:utf-8
# author:YJ沛

'''
虚拟环境命令：
    安装virtualenv虚拟环境方法一：：pip install virtualenv
    安装virtualenv虚拟环境方法二：pip install virltualenvwrapper-win
    查看已创建的虚拟环境：workon
    创建：mkvirtualenv [虚拟环境名称]
    删除：rmvirtualenv [虚拟环境名称]
    进入：workon [虚拟环境名称]
    退出：deactivate
    查看已安装的库：pip list    、pip freeze

django的命令：
    创建一个项目：django-admin startproject
    生成一个应用：python manage.py startapp
    生成移交：python manage.py makemigrations
    移交：python manage.py migrate
    启动服务器：python manage.py runserver
    创建超级用户：python manage.py createsuperuser

admin的使用admin.py
    注册：admin.site.register(模型类，admin类)

    自定义管理页面：
        class QuestionAdmin(admin.ModelAdmin):
            ...
        admin.site.register(Question, QuestionAdmin)

    列表页属性：
        list_display：显示字段，可以点击列头进行排序
        list_filter：过滤字段，过滤框会出现在右侧
        search_fields：搜索字段，搜索框会出现在上侧
        list_per_page：分页，分页框会出现在下侧
        fields：属性的先后顺序
        fieldsets：属性分组

    关联对象：
        1，对于HeroInfo模型类，有两种注册方式
            方式一：与BookInfo模型类相同
            方式二：关联注册
        2，可以将内嵌的方式改为表格：



'''
