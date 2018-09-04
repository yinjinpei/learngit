#-*- coding:utf-8 -*-
#author:YJ沛


class Test(object):
    def __init__(self,function):
        print("----- 初始化 ------")
        print("----- function name is %s"%function.__name__)
        self.__function = function

    def __call__(self):
        print("--------- 装饰器中的功能 ---------")
        self.__function()


@Test       #等同于 test=Test(test)
def test():
    print("-------- test ----------")

test()