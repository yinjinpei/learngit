#-*- coding:utf-8 -*-
#author:YJ沛

'''
__getattribute__:类属性访问拦截器,不能返回属性，不然会死循环.

'''

class Test(object):
    def __init__(self):
        self.subject1 = "subject1"
        self.subject2 = "peter"

    def __getattribute__(self,item):   #属性访问拦截器，调用属性时会先执行这个函数，相当把这个属性传进来判断
        if item == "subject1":
            print("log: 非法访问属性！！！")
            return "不允许访问该属性，请勿尝试！！"
        else:
            return object.__getattribute__(self,item)   #为不影响程序，返回这个属性的值，不能返回属性，不然会死循环：如self.show

    def show(self):
        print("-------------test ----------")


a = Test()
print(a.subject1)
print(a.subject2)

a.show()    #调用方法分二步，1.先获取show属性对应的结果，应该是一个方法。 2，方法（）




print("############################# 分割线 ######################################")

class Test(object):
    def __init__(self):
        self.subject1 = "subject1"
        self.subject2 = "peter"

    def __getattribute__(self,item):   #属性访问拦截器，调用属性时会先执行这个函数，相当把这个属性传进来判断
        print("----1 %s ----"%item)
        if item == "subject1":
            print("log: 非法访问属性！！！")
            return "不允许访问该属性，请勿尝试！！"
        else:
            temp = object.__getattribute__(self,item)   #为不影响程序，返回这个属性的值
            print("----1 %s ----" % temp)
            return temp

            #return object.__getattribute__(self,item)   #为不影响程序，返回这个属性的值，不能返回属性，不然会死循环

    def show(self):
        print("-------------test ----------")


a = Test()
print(a.subject1)
print(a.subject2)

a.show()    #调用方法分二步，1.先获取show属性对应的结果，应该是一个方法。 2，方法（）