#-*- coding:utf-8 -*-
#author:YJ沛

#例子不修改原代码，扩展功能：
#原有功能：
# def f1():
#     print("------- f1 -------")
#
# def f2():
#     print("------- f2 -------")

#新增功能,新增验证,方法一(使用了闭包)：
# def w1(func):
#     def inner():
#         print("----正在验证--------")
#         func()
#     return inner

#调用
# innerFunc = w1(f1)
# innerFunc()

# innerFunc = w1(f2)
# innerFunc()

import random
#新增功能,新增验证,方法二(使用了闭包)：
def w2(func):
    def inner():
        print("----正在验证--------")
        if random.randint(1,10) == 1:    #设置条件
            func()
        else:
            print("---- 验证不通过----")

    return inner

#原有功能：
# @w2相当 f1 = w2(f1)
@w2
def f1():
    print("------- f1 -------")
@w2
def f2():
    print("------- f2 -------")


#调用
f1()
f2()


