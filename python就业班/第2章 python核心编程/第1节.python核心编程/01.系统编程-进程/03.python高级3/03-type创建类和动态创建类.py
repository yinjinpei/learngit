#-*- coding:utf-8 -*-
#author:YJ沛

#动态创建类，一般不这怎么用

def test(name):
    if name == "Test1":
        class Test1(object):
            def print_info(self):
                print('------ Test1 -----')
        return Test1

    elif name == "Test2":
        class Test2(object):
            def print_info(self):
                print('-------- Test2 --------')
        return Test2

t1 = test("Test1")
t2 = test("Test2")
t1.print_info("xxx")
t2.print_info("xxxx")



