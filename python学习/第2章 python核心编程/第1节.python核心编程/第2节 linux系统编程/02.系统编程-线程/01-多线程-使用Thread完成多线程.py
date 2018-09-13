#-*- coding:utf-8 -*-
#author:YJ沛

'''
线程的  执行顺序是无序的！
'''

from threading import Thread
import time
import os

print("###################  方法一 #################")
def test():
    print("写个毛球！！！")
    print(t.name)
    time.sleep(1)

for i in range(5):
    t = Thread(target=test) # 如果多个线程执行同一个函数，各自线程互不影响
    t.start()
print('-----主线程----')


print("###################  方法二 #################")
class MyThread(Thread):
    def run(self):
        for i in range(5):
            time.sleep(1)
            msg = "I am "+self.name+" @ "+str(i)    # name属性中保存的是当时线程的名字
            print(msg)

if __name__ == "__main__":
    t = MyThread()
    t.start()

    t2 = MyThread()
    t2.start()