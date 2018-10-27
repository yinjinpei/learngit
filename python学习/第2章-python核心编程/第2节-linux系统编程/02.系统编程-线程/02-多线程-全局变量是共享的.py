#-*- coding:utf-8 -*-
#author:YJ沛

'''
线程的 执行顺序是无序的！
全局变量线程之间是共享的！
'''

from threading import Thread
import time


num = 100
def test():
    for i in range(3000000):
        global num
        num += 1
    print("---------test num:%d ---------"%num)

def test2():
    global num
    print("---------test2 num:%d ---------" % num)


print("--------- num:%d ---------" % num)
t = Thread(target=test)
t.start()

# time.sleep(1)   # 睡眠1秒，保证test()执行完毕

t2 = Thread(target=test2)
t2.start()

'''
执行结果：说明全局变量线程之间是共享的！
--------- num:100 ---------
--------- num:103 ---------
--------- num:103 ---------
'''

time.sleep(2)

print('########################################################')

num = 100
def test():
    for i in range(1000000):
        global num
        num += 1
    print("---------test num:%d ---------"%num)

def test2():
    for i in range(1000000):
        global num
        num += 1
    print("---------test2 num:%d ---------"%num)


print("--------- num:%d ---------" % num)
t = Thread(target=test)
t.start()

# time.sleep(3)  #取消注释结果会不一样，

t2 = Thread(target=test2)
t2.start()

'''
执行结果： 说明理论上应该是test2 num是2000100，但由于有两个函数在运算，和系统调试问题导致数据不对
--------- num:100 ---------
---------test num:1228325 ---------
---------test2 num:1210598 ---------
'''