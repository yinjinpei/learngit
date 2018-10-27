#-*- coding:utf-8 -*-
#author:YJ沛

'''
锁：等待解锁的方式：通知模式
    一个释放，所有都在抢
死锁解决方法：1，加上超时时间 2，银行家算法

'''

from threading import Thread,Lock
import time

print('########################## 以下解决死锁 ########################')
class Test1(Thread):
    def run(self):
        if mutestA.acquire():   #可以上锁则返回True
            print('----------%s mutestA已上锁---------'%self.name)
            time.sleep(1)

        if mutestB.acquire(True,2):   #True表示堵塞状态，2表示2秒超时，2秒后不堵塞，直接跳过（if里面代码不执行），继续往下执行
            print('--------- %s mutestB已上锁---------'%self.name)
            mutestB.release()
        mutestA.release()


class Test2(Thread):
    def run(self):
        if mutestB.acquire():
            print('----------%s mutestA已上锁---------' % self.name)
            time.sleep(1)

        if mutestA.acquire():
            print('--------- %s mutestB已上锁---------' % self.name)
            mutestA.release()
        mutestB.release()

mutestA = Lock()
mutestB = Lock()

t1 = Test1()
t1.start()

t2 = Test2()
t2.start()