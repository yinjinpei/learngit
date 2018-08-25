#-*- coding:utf-8 -*-
#author:YJ沛

'''
闭包： 有函数内部再定义一个函数，并且这个函数用到了外边函数的变量，那么将这个函数以及用到的一些变量称之为闭包
特点：1，外边函数返回里边函数的引用
     2，里面函数调用外边函数的变量

'''
#例1：
def test(number):
    def test_in(number_in):
        print(number_in)
        return number+number_in
    return test_in

ret = test(20)  #这个20 是给test函数的
print(ret(30))  #这里20 是给test_in函数的

#例2:
def test2(number_2):
    print("-----test2-------")

    def test2_in():
        print("-------- test_in----------")
        return number_2 + 100
    return test2_in

b = test2(20)
print(b())