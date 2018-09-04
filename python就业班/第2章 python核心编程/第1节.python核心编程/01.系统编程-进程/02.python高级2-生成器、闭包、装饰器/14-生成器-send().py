#-*- coding:utf-8 -*-
#author:YJ沛


print('-------------------- 斐波拉契数列 --------------------')
################## 斐波拉契数列 ########################
'''
除了第一个和第二个数外，任意一个都可由前两个数相加得到：1,2,3,5,8,12,21,34
'''
def fib():
    a,b = 0,1
    for i in range(9):
        temp = yield b
        print(temp)
        a,b = b,a+b

print('------------ 读取方法一 --------------')
a = fib()
for i in a:
    print(i)


print('------------ 读取方法二 --------------')
b = fib()
for i in range(9):
    print(next(b))


print('------------ 读取方法三 --------------')
c = fib()
for i in range(9):
    print(c.__next__())


print('------------ 读取方法四 --------------')
#使用 send()
c = fib()

c.send(None)        #在使用send之前要先使用next或者send(None)不然要报错
for i in range(8):  #注意，这里是 8 ，因为send(None)已经执行一次了
    print(c.send('dd'))

