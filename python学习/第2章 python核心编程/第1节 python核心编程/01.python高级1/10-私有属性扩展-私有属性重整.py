#-*- coding:utf-8 -*-
#author:YJ沛

print("################## 获取、修改私有属性方法三 #################")
class Money:
    def __init__(self):
        self.__money = 1000
        self.__num = 200

m = Money()

print(dir(m))
'''执行结果如下：
['_Money__money', '_Money__num', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

从结果可以看到，私有属性名称被重命名了:
__money 变成 _Money__money
__num   变成 _Money__num

'''

print(m._Money__money)  #实际开发中不这样用。
print(m._Money__num)

