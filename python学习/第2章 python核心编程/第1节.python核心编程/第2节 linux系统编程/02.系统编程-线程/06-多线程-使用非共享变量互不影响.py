#-*- coding:utf-8 -*-
#author:YJ沛

'''
锁：等待解锁的方式：通知模式
    一个释放，所有都在抢
'''

from threading import Thread
import threading
import time


def test():
    name = threading.current_thread().name  #获取线程名字
    print('这个线程名字为：%s'%name)
    num = 100

    if name == 'Thread-1':  # 判断，如果是线程名为Thread-1则执行 num+1,否则其它线程不加1
        num += 1
    else:
        time.sleep(1)
    print("----这个线程名字为：%s -----test num:%d ---------"%(name,num))

t = Thread(target=test)
t.start()

t2 = Thread(target=test)
t2.start()

'''
执行结果：   说明多线程使用非共享变量互不影响
这个线程名字为：Thread-1
----这个线程名字为：Thread-1 -----test num:101 ---------
这个线程名字为：Thread-2
----这个线程名字为：Thread-2 -----test num:100 ---------
'''