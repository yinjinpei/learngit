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
        print("----- test_in ------")
        return number_2 + 100
    return test2_in

b = test2(20)
print(b())



print("-"*50)
############### 应用 ###################
#原先方法：
def createNum(a,b,x):
    print(a*x+b)

a = 1
b = 1
x = 0
createNum(a,b,x) #缺点：每次都要传三个参数

#使用闭包函数
def createNum2(a,b):
    def createNum_in(x):
        print(a*x+b)
    return createNum_in

#闭包优点：不需要每次都传三个实参
num = createNum2(1,1)
num(0)
num(2)

num2 = createNum2(2,2)
num(0)
num(10)






