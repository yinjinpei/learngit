#-*- coding:utf-8 -*-
#author:YJ沛

'''
__slots__作用:
在Python中，当我们定义了一个class，创建了一个class的实例后，我们可以给该实例绑定任何属性和方法，当你需要限制可绑定的实例的属性的时候， 就可以使用__slots__。

'''

class Person(object):
    __slots__ = ("name","age")


P = Person()
P.name = "peter"
P.age = 18
print(P.name);print(P.age)

P.job = 'IT'    #添加不了，因为__slots__做了限制，不包含job属性

