#-*- coding:utf-8 -*-
#author:YJ沛

'''
线程的 执行顺序是无序的！
全局变量线程之间是共享的！
'''

from threading import Thread
import time


def test(listName):
    listName.append(100)
    print("---------test listName:%s ---------"%listName)

def test2(listName):
    print("---------test2 listName:%s ---------" % listName)


list = [1,2,3,4,5]
print("--------- list:%s ---------" % list)
t = Thread(target=test,args=(list,))
t.start()

time.sleep(1)   # 睡眠1秒，保证test()执行完毕

t2 = Thread(target=test2,args=(list,))
t2.start()

'''
执行结果：列表也是共享的！
--------- list:[1, 2, 3, 4, 5] ---------
---------test num:[1, 2, 3, 4, 5, 100] ---------
---------test2 num:[1, 2, 3, 4, 5, 100] ---------
'''