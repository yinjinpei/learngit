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
#需要在Linux上或mac上运行
import os
import time

num = 100

ret = os.fork()     # 返回值 父进程大于0，新的子进程为0
if ret == 0:    # 子进程
    num += 100
    print(num)

else:   # 父进程
    time.sleep(3)
    print(num)


#结果：   200
#        100