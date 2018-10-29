#-*- coding:utf-8 -*-
#author:YJ沛

from multiprocessing import Pool
import time
import os


def test(num):
    for i in range(5):
        print('------- pid: %d ----- num=%d------'%(os.getpid(),num))
        time.sleep(1)

if __name__ == "__main__":

    p = Pool(3) #3表示进程池中最多有3个进程同时执行

    for i in range(10):
        print('-------- %d --------'%i)

        ''' 向进程池中添加任务
            注意：如果添加的任务数量超过了进程池中进程的个数，那么不会导致添加不进入。
            添加到进程中的任务，如果还没有被执行的话，那么此时他们会等待进程池中的进程完成一个任务之后，会自动的去用刚刚的那个进程，
            来完成当前的新任务
        '''
        p.apply(test,(i,))    #堵塞方法，参数用元组表示

    # 关闭进程池，相当于不能够再次添加新任务了
    p.close()

    '''主进程创建或添加任务后，主进程默认不会等待进程池中的任务执完成才结束，而是当主进程的任务做完之后立马结束。
       如果这里没有join，会导致进程池中的任务不会被执行
    '''
    p.join()