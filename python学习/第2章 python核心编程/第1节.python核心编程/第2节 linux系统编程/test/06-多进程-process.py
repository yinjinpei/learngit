#-*- coding:utf-8 -*-
#author:YJ沛

'''
和fork 函数功能一样是多，但process可以跨平台，用法有点不同

start()方法启动，这样创建进程比fork()还要简单。
join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。（进一步地解释，哪个子进程调用了join方法，
主进程就要等该子进程执行完后才能继续向下执行，具体可见下边的分析图）

程序无法正常运行，之后根据报错信息，修改部分代码，在多进程模块放在if __name__ == '__main__':内，即可正常运行，原理不明

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

'''


from multiprocessing import Process
import time


def test():
    while True:
        print('--------------- test ------------------')
        time.sleep(1)


def main():
    p = Process(target=test)
    p.start()

    while True:
        print('------------ 主进程-----------------')
        time.sleep(1)

if __name__ == "__main__":
    main()