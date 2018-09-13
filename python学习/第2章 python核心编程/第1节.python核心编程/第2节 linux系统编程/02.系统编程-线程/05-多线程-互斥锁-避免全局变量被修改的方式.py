#-*- coding:utf-8 -*-
#author:YJ沛


from threading import Thread,Lock
import time

g_num = 100


def test():
    global g_num

    mutex.acquire() # 上锁，这个线程和test2线程都在抢着对这个锁进行上锁，如果有一方成功上锁，
                    # 那么导致另一方堵塞（一直等待）到这个锁被解开为止

    for i in range(1000000):
        g_num += 1

    mutex.release() # 解锁，用来对mutex指向的这个锁进行解锁，只有开了锁，
                    # 那么接下来会让所有因为这个锁被上了锁而堵塞的线程进行抢着上锁

    print("---------test num:%d ---------"%g_num)

def test2():
    global g_num

    mutex.acquire()  # 上锁

    for i in range(1000000):
        g_num += 1

    mutex.release()  # 解锁
    print("---------test2 num:%d ---------"%g_num)


# 创建互斥锁，这个锁默认是没有上锁的
mutex = Lock()

print("--------- num:%d ---------" % g_num)
t = Thread(target=test)
t.start()


t2 = Thread(target=test2)
t2.start()
