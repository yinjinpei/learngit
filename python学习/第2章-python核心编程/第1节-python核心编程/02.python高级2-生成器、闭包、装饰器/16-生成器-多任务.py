#-*- coding:utf-8 -*-
#author:YJ沛


def test_1():
    while True:
        print("--- 1 ---")
        yield None

def test_2():
    while True:
        print("--- 2 ---")
        yield None


t1 = test_1()
t2 = test_2()


def test():
    while True:
        t1.__next__()
        t2.__next__()

test()  #此时有三个while在跑，形成多任务，协程