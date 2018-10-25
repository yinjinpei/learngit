#-*- coding:utf-8 -*-
#author:YJ沛

'''协程
计算密集型：需要占用大量的cpu资源----多进程实现
io密集型（协程）：需要网络功能，大量的时间都在等待网络数据的到来 ----多线程，协程实现

'''

import time


def A():
    while True:
        print("------ A -------")
        yield
        time.sleep(0.5)

def B(c):
    while True:
        print("------ B -------")
        next(c)
        #c.__next__()
        time.sleep(0.5)


if __name__ == "__main__":
    a = A()
    B(a)
