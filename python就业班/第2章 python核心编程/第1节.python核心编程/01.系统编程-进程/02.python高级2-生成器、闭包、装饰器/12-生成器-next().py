#-*- coding:utf-8 -*-
#author:YJ沛


#生成一个列表：
a = [ x*2 for x in range(10) ]
print(a)

#生成器表示方式一：
b = (x*2 for x in range(10))    #得到一个对象的地址
print(b)

#取值方法一：(使用 next() 函数)
a = 1
while a < 11:       #超出读取范围将出现异常 比如 a < 12
    print(next(b))  #利用 next函数读取生成器
    a+=1


#生成器表示方式二（使用yield）：
print('-------------------- 斐波拉契数列 --------------------')
################## 斐波拉契数列 ########################
'''
除了第一个和第二个数外，任意一个都可由前两个数相加得到：1,2,3,5,8,12,21,34
'''
def fib(times):
    n = 0
    a,b = 0,1
    while n < times:
        yield b     #生成器表示方法二，此函数称为生成器
        a,b = b,a+b
        n+=1

#创建生成器对象 a
a = fib(9)
print(a)

#取值方法一：
for i in a:
    print(i)

print('-------------------------------')
#取值方法二：(使用 __next__() 函数，)
b = fib(9)
for i in range(9):
    print(next(b))

print('-------------------------------')
#取值方法三：(使用 __next__() 函数 或next() 函数，两个函数方式是一样的)
b = fib(9)
for i in range(9):
    ret = b.__next__()
    print(ret)

#使用 __next__() 函数 或next() 函数，两种方式是一样的)