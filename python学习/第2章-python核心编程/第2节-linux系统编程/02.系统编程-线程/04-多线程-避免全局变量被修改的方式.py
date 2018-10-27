#-*- coding:utf-8 -*-
#author:YJ沛

'''
线程的 执行顺序是无序的！
全局变量线程之间是共享的！
'''

from threading import Thread
import time

g_num = 100
g_flag = True

def test():
    global g_flag
    global g_num
    if g_flag:
        for i in range(1000000):
            g_num += 1
        g_flag = False

    print("---------test num:%d ---------"%g_num)

def test2():
    #方法二：轮询，判断g_flag有没有被修改了，如果修改了说明test执行完了
    while True:
        if g_flag:
            time.sleep(0.5)   # 减少Cpu负担
            continue
        else:
            break

    for i in range(1000000):
        global g_num
        g_num += 1

    print("---------test2 num:%d ---------"%g_num)


print("--------- num:%d ---------" % g_num)
t = Thread(target=test)
t.start()

#方法一：
# time.sleep(3)  #取消注释结果会不一样，

t2 = Thread(target=test2)
t2.start()
