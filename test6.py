#-*- coding:utf-8 -*-
#author:YJ沛
from threading import Timer,Thread
import threading
def test():
    print(' The Tread name is %s ---------'%threading.current_thread().name)
    t = Timer(2, test)
    t.start()

# test()
t = Timer(2, test)
t.start()