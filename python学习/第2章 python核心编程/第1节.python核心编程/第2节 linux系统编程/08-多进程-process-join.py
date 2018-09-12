#-*- coding:utf-8 -*-
#author:YJ沛

'''
Process语法结构如下：
Process([group [, target [, name [, args [, kwargs]]]]])

target：表示这个进程实例所调用对象；

args：表示调用对象的位置参数元组；

kwargs：表示调用对象的关键字参数字典；

name：为当前进程实例的别名；

group：大多数情况下用不到；

Process类常用方法：

is_alive()：判断进程实例是否还在执行；

join([timeout])：是否等待进程实例执行结束，或等待多少秒；

start()：启动进程实例（创建子进程）；

run()：如果没有给定target参数，对这个对象调用start()方法时，就将执行对象中的run()方法；

terminate()：不管任务是否完成，立即终止；

Process类常用属性：

name：当前进程实例别名，默认为Process-N，N为从1开始递增的整数；

pid：当前进程实例的PID值；

程序无法正常运行，之后根据报错信息，修改部分代码，在多进程模块放在if __name__ == '__main__':内，即可正常运行，原理不明
'''


from multiprocessing import Process
import time
import os

def test(args):
    for i in range(5):

        print('---- test ---- 子进程：%d ==== 父进程: %d-----'%(os.getpid(),os.getppid()),args)
        time.sleep(1)


def main():
    p = Process(target=test,args=('100',))
    p.start()

    for i in range(2):
        print('---- 主进程 ---- 父进程：%d ==== 父父进程: %d-----' % (os.getpid(), os.getppid()))
        time.sleep(1)

    p.join(2)   # 主进程等待2秒 子进程，2秒后子进程还没结束就不等了，继续往下执行

    print('--------- 主进程 ----------')

if __name__ == "__main__":
    main()

'''
结果: 说明父进程结果后并没有退出，而是在等子进程结果后退出
---- 主进程 ---- 父进程：12144 ==== 父父进程: 592-----
---- test ---- 子进程：11124 ==== 父进程: 12144-----
---- 主进程 ---- 父进程：12144 ==== 父父进程: 592-----
---- test ---- 子进程：11124 ==== 父进程: 12144-----
---- test ---- 子进程：11124 ==== 父进程: 12144-----
---- test ---- 子进程：11124 ==== 父进程: 12144-----
---- test ---- 子进程：11124 ==== 父进程: 12144-----

'''