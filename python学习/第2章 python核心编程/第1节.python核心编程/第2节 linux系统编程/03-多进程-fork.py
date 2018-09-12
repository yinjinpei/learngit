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

ret = os.fork()     # 返回值 父进程大于0，新的子进程为0
if ret == 0:    # 子进程
    print(ret)
    while True:
        print('----- 1 -------子进程 PID :%d-----父进程PID :%d '%(os.getpid(),os.getppid()))
        time.sleep(1)
else:   # 父进程
    print(ret)
    while True:
        print('----- 2 -------父进程PID :%d ---------- 父父进程PID: %d'%(os.getpid(),os.getppid()))

        time.sleep(1)
