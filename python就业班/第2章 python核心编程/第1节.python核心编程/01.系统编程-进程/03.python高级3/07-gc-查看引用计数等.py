#-*- coding:utf-8 -*-
#author:YJ沛

'''
sys.getrefcount()  : #查看引用个数，数字减1才是真实的，因为这个函数本身就引用了1个

gc.get_count() ：#获取当前自动执行垃圾回收的计数器，返回一个长度为3的列表

gc.get_threshold() ：#获取的gc模块中自动执行垃圾回收的频率

gc.set_threshold()  ：#设置自动执行垃圾回收的频率

gc.disable()  :  #默认关掉gc垃圾回收功能

gc.enable() :  #默认开启gc垃圾回收功能

gc.collect()  : #手动开启gc垃圾回收功能

gc.garbage  ：#查看被回收的对象信息

注意：如果类里重写了 __del__() 方法,需要调用父类释放空间方法，因为gc释放空间正是调用 __del__()方法的，被重写就不会删除了，需要手动

'''
import time
import gc
import sys

print(gc.get_count())       #(329, 11, 0)   当第一个数达到700，刚会清理1代，第二个数为1代清理次数，第三个是2代清理次数

print(gc.get_threshold())   #执行结果：(700, 10, 10)   当创建的对象数量减去已经回收对象数量的差大于700时触发0代链表清理，
                            #当0代链表清理了10次，则清理1代链表，当1代链表清理10次，则清理2代链表

b =1
print(sys.getrefcount(b))   #

class Test(object):
    def __init__(self):
        print('---- test -------')

def foo():
    a = 0
    while a < 5:
        t1 = Test()
        t2 = Test()
        t1.num = t2
        t2.num = t1
        print(sys.getrefcount(a))

        gc.collect()     #手动开启gc垃圾回收功能
        a +=1
        time.sleep(1)
        print(gc.get_count())

gc.disable()    #默认关掉gc垃圾回收功能
foo()

gc.set_threshold(500,2,2)   #设置自动执行垃圾回收的频率


print(gc.garbage)