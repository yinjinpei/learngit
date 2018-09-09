#-*- coding:utf-8 -*-
#author:YJ沛

'''
单核CPU多任务运行：
    调度算法：
        时间片轮转
        优先级调度

    并发：相当任务数多于单核数
    并行：真正一起运行
'''

import os
import time

ret = os.fork()
if ret == 0:
    print(ret)
    while True:
        print('----- 1 -------')
        time.sleep(1)
else:
    print(ret)
    while True:
        print('----- 2 -------')
        time.sleep(1)
