#-*- coding:utf-8 -*-
#author:YJ沛

from multiprocessing import Process
import time

class MyNewprocess(Process):
    def run(self):
        while True:
            print('---------- 1-----------')
            time.sleep(1)

if __name__ == "__main__":
    p = MyNewprocess()
    p.start()
    p.join(3 )
    while True:
        print('-----------2 -----------')
        time.sleep(1)
