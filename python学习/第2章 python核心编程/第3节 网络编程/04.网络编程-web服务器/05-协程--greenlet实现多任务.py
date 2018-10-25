#-*- coding:utf-8 -*-
#author:YJ沛

'''协程--greenlet实现多任务

'''

import time
from greenlet import greenlet


def test1():
    while True:
        print("------ test1 --------")
        gr2.switch()    # 执行此行时会跳到test2执行
        time.sleep(0.5)

def test2():
    while True:
        print("------ test2 --------")
        gr1.switch()    # 执行此行时会跳到test1执行
        time.sleep(0.5)

gr1 = greenlet(test1)
gr2 = greenlet(test2)

gr1.switch()    # 执行此行时会跳到test1执行