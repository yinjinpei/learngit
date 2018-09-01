#-*- coding:utf-8 -*-
#author:YJ沛


class Person(object):
    def __init__(self,newName,newAge):
        self.name = newName
        self.age = newAge

    def eat(aa):
        print("------- %s 在吃饭 --------"%aa.name)

def peter_run(self):
    print("------- %s 在跑步 --------" % self.name)

def run(self):
    print("------- %s 在奔跑 --------" % self.name)

@staticmethod
def test():
    print("----- static method ------")

@classmethod
def test2(cls):
    print("------- class method -------")


alex = Person("alex",22)
peter = Person("peter",18)

#把外面peter_run方法添加到peter对象中，只能给peter对象用，其他对象用不了
import types
peter.peter_run = types.MethodType(peter_run,peter)
peter.peter_run()

#把外面run方法添加到类中：
Person.run = run
peter.run()
alex.run()

#把静态方法test()添加到类中：
Person.test = test
Person.test()
peter.test()
alex.test()

#把类方法test2()添加到类中：
Person.test2 = test2
Person.test2()
peter.test2 ()
alex.test2()






