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
    创建一个项目：django-admin startproject 项目名
    生成一个应用：python manage.py startapp 应用名
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


定义模型
    1,在模型中定义属性，会生成表中的字段
    2,django根据属性的类型确定以下信息：
        当前选择的数据库支持字段的类型
        渲染管理表单时使用的默认html控件
        在管理站点最低限度的验证
    3,django会为表增加自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置某属性为主键列后，则django不会再生成默认的主键列
    4,属性命名限制
        不能是python的保留关键字
        由于django的查询方式，不允许使用连续的下划线

定义属性
    1,定义属性时，需要字段类型
    2,字段类型被定义在django.db.models.fields目录下，为了方便使用，被导入到django.db.models中
    3,使用方式
        1)导入from django.db import models
        2)通过models.Field创建字段类型的对象，赋值给属性
    4,对于重要数据都做逻辑删除，不做物理删除，实现方法是定义isDelete属性，类型为BooleanField，默认值为False

字段类型
    1，AutoField：一个根据实际ID自动增长的IntegerField，通常不指定,如果不指定，一个主键字段将自动添加到模型中
    2，BooleanField：true/false 字段，此字段的默认表单控制是CheckboxInput
    3，NullBooleanField：支持null、true、false三种值
    4，CharField(max_length=字符长度)：字符串，默认的表单样式是 TextInput
    5，TextField：大文本字段，一般超过4000使用，默认的表单控件是Textarea
    6，IntegerField：整数

    7，DecimalField(max_digits=None, decimal_places=None)：使用python的Decimal实例表示的十进制浮点数
        1)DecimalField.max_digits：位数总数
        2)DecimalField.decimal_places：小数点后的数字位数

    8，FloatField：用Python的float实例来表示的浮点数
    9，DateField[auto_now=False, auto_now_add=False])：使用Python的datetime.date实例表示的日期
        1)参数DateField.auto_now：每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为false
        2)参数DateField.auto_now_add：当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为false
        3)该字段默认对应的表单控件是一个TextInput. 在管理员站点添加了一个JavaScript写的日历控件，和一个“Today"的快捷按钮，包含了一个额外的invalid_date错误消息键
        4)auto_now_add, auto_now, and default 这些设置是相互排斥的，他们之间的任何组合将会发生错误的结果

    10，TimeField：使用Python的datetime.time实例表示的时间，参数同DateField
    11，DateTimeField：使用Python的datetime.datetime实例表示的日期和时间，参数同DateField
    12，FileField：一个上传文件的字段
    13，ImageField：继承了FileField的所有属性和方法，但对上传的对象进行校验，确保它是个有效的image

字段选项
通过字段选项，可以实现对字段的约束
在字段对象时通过关键字参数指定
null：如果为True，Django 将空值以NULL 存储到数据库中，默认值是 False
blank：如果为True，则该字段允许为空白，默认值是 False
对比：null是数据库范畴的概念，blank是表单验证证范畴的
db_column：字段的名称，如果未指定，则使用属性的名称
db_index：若值为 True, 则在表中会为此字段创建索引
default：默认值
primary_key：若为 True, 则该字段会成为模型的主键字段
unique：如果为 True, 这个字段在表中必须有唯一值
关系
关系的类型包括
ForeignKey：一对多，将字段定义在多的端中
ManyToManyField：多对多，将字段定义在两端中
OneToOneField：一对一，将字段定义在任意一端中
可以维护递归的关联关系，使用'self'指定，详见“自关联”
用一访问多：对象.模型类小写_set
bookinfo.heroinfo_set
用一访问一：对象.模型类小写
heroinfo.bookinfo
访问id：对象.属性_id
heroinfo.book_id
元选项
在模型类中定义类Meta，用于设置元信息
元信息db_table：定义数据表名称，推荐使用小写字母，数据表的默认名称
<app_name>_<model_name>
ordering：对象的默认排序字段，获取对象的列表时使用，接收属性构成的列表
class BookInfo(models.Model):
    ...
    class Meta():
        ordering = ['id']
字符串前加-表示倒序，不加-表示正序
class BookInfo(models.Model):
    ...
    class Meta():
        ordering = ['-id']
排序会增加数据库的开销
示例演示
创建test2项目，并创建booktest应用，使用mysql数据库
定义图书模型
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()
    bread = models.IntegerField(default=0)
    bcommet = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)
英雄模型
class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    hcontent = models.CharField(max_length=100)
    hbook = models.ForeignKey('BookInfoBookInfo')
定义index、detail视图
index.html、detail.html模板
配置url，能够完成图书及英雄

'''
