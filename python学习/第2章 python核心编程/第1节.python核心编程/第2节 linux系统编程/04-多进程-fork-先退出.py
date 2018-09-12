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
    print('------ 子进程 PID: %d---------' % os.getpid())
    print('---------- 哈哈1 ----------')
    print('---------- 哈哈2 ----------')
    print('---------- 哈哈3 ----------')
    time.sleep(3)
else:   # 父进程
    print('------ 父进程 PID: %d---------' % os.getpid())
    print('---------- 呵呵1 ----------')
    print('---------- 呵呵2 ----------')
    print('---------- 呵呵3 ----------')
    time.sleep(1)

print('------ over PID: %d------ PPID: %d---'%(os.getpid(),os.getppid()))




