# coding:utf-8
# author:YJ沛


#题目：执行print(Foo().think.different.itcast)， 并不显示后面信息<__main__.Foo object at 0x02D27810>


class Foo(object):
    def __init__(self):
        pass

    # 当在__dict_中没有找到属性时就会执行这个方法
    def __getattr__(self, item):
        print(item)
        return  self

    def __str__(self):

        '''最后打印不返回对象的地址'''
        return ''


print(Foo().think.different.itcast)

a = Foo()
a.think.different.itcast