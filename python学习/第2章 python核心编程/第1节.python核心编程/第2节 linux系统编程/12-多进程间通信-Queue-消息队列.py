#-*- coding:utf-8 -*-
#author:YJ沛

from multiprocessing import Pool,managers,Queue
import time
import os
import random


'''
Queue,消息队列特点：先进先出，后进后出
栈的特点：先进后出，后进先出

Queue.qsize()：返回当前队列包含的消息数量；

Queue.empty()：如果队列为空，返回True，反之False ；

Queue.full()：如果队列满了，返回True,反之False；

Queue.get([block[, timeout]])：获取队列中的一条消息，然后将其从列队中移除，block默认值为True；

1）如果block使用默认值，且没有设置timeout（单位秒），消息列队如果为空，此时程序将被阻塞（停在读取状态），直到从消息列队读到消息为止，
    如果设置了timeout，则会等待timeout秒，若还没读取到任何消息，则抛出"Queue.Empty"异常；

2）如果block值为False，消息列队如果为空，则会立刻抛出"Queue.Empty"异常；

Queue.get_nowait()：相当Queue.get(False)；

Queue.put(item,[block[, timeout]])：将item消息写入队列，block默认值为True；

1）如果block使用默认值，且没有设置timeout（单位秒），消息列队如果已经没有空间可写入，此时程序将被阻塞（停在写入状态），
    直到从消息列队腾出空间为止，如果设置了timeout，则会等待timeout秒，若还没空间，则抛出"Queue.Full"异常；

2）如果block值为False，消息列队如果没有空间可写入，则会立刻抛出"Queue.Full"异常；

Queue.put_nowait(item)：相当Queue.put(item, False)；
'''

q = Queue(3)    # 初始化一个Queue对象，最多可接收三条put消息

q.put("消息1")    #存放一个消息
print(q.full()) # False,还没满
q.put("消息2")
q.put("消息3")

print(q.full()) # True  已满
print(q.empty())    # False 非空

# 当储存满了继续存放消息，则会抛出异常
try:
    q.put("消息4", True, 2)   #储存：消息4，2表示2秒后储存不了则抛出异常
except Exception:
    print("已满，不能再储存了，请先取值！！")

print(q.get()) #取一个值,取值从最先进的开始取
print(q.get())
print(q.get())
