#-*- coding:utf-8 -*-
#author:YJ沛


def test():
    global a
    a = 100
    print(a)

test()
print(a)

import random

print(random.random())


class NameError(Exception):
    print('11111111111')


try:
    s = None
    if s is None:
        print("s 是空对象")

        raise NameError  # 如果引发NameError异常，后面的代码将不能执行

except NameError:
    print('1111111111111111111')
except TypeError:
    print("空对象没有长度")
