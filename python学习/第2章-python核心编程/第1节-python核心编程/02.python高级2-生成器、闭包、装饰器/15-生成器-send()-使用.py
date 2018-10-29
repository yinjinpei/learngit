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


print('------------ 读取方法四 --------------')
#使用 send()
c = fib()

c.send(None)        #在使用send之前要先使用next或者send(None)不然要报错
print(c.send('haha'))
print(c.send('hehe'))
print(c.send('peter'))
print(c.send('alex'))


print('------------ 扩展 --------------')
#扩展
def test():
    i = 0
    while i < 5:
        if i == 0:
            temp = yield i
        else:
            yield i
        print(temp)
        i += 1

t = test()
t.send(None)
t.send("haha")
t.send("hehe")  #此时打印的还是上次结果 haha