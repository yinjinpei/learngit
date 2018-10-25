#-*- coding:utf-8 -*-
#author:YJ沛


'''gevent版服务器
greenlet已经实现了协程，但是这个还的人工切换，是不是觉得太麻烦了，不要捉急，python还有一个比greenlet更强大的并且能够自动切换任务的
模块gevent

其原理是当一个greenlet遇到IO(指的是input output 输入输出，比如网络、文件操作等)操作时，比如访问网络，就自动切换到其他的greenlet，
等到IO操作完成，再在适当的时候切换回来继续执行。

由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO

注意: 需要安装gevent库
'''


import gevent

def test1(a):
    for i in range(a):
        print(gevent.getcurrent(), i)

        # 用来模拟一个耗时操作，注意不是time模块中的sleep
        gevent.sleep(0.5)

# 创建三个
ge1 = gevent.spawn(test1, 5)
ge2 = gevent.spawn(test1, 6)
ge3 = gevent.spawn(test1, 7)

ge1.join()
ge2.join()
ge2.join()