#-*- coding:utf-8 -*-
#author:YJ沛

'''
和fork 函数功能一样是多，但process可以跨平台，用法有点不同

start()方法启动，这样创建进程比fork()还要简单。
join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。（进一步地解释，哪个子进程调用了join方法，
主进程就要等该子进程执行完后才能继续向下执行，具体可见下边的分析图）

程序无法正常运行，之后根据报错信息，修改部分代码，在多进程模块放在if __name__ == '__main__':内，即可正常运行，原理不明
'''


from multiprocessing import Process
import time
import os

def test():
    for i in range(5):
        print('---- test ---- 子进程：%d ==== 父进程: %d-----'%(os.getpid(),os.getppid()))
        time.sleep(1)


def main():
    p = Process(target=test)
    p.start()

    for i in range(2):
        print('---- 主进程 ---- 父进程：%d ==== 父父进程: %d-----' % (os.getpid(), os.getppid()))
        time.sleep(1)

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