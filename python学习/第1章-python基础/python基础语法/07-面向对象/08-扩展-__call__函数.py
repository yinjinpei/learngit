#-*- coding:utf-8 -*-
#author:YJ沛

'''
Python中的函数是一级对象。这意味着Python中的函数的引用可以作为输入传递到其他的函数/方法中，并在其中被执行。
而Python中类的实例（对象）可以被当做函数对待。也就是说，我们可以将它们作为输入传递到其他的函数/方法中并调用他们，
正如我们调用一个正常的函数那样。而类中__call__()函数的意义正在于此。为了将一个类实例当做函数调用，
我们需要在类中实现__call__()方法。也就是我们要在类中实现如下方法：def __call__(self, *args)。这个方法接受一定数量的变量作为输入。
假设x是X类的一个实例。那么调用x.__call__(1,2)等同于调用x(1,2)。这个实例本身在这里相当于一个函数。
'''

class X(object):
    def __init__(self, a, b, range):
        self.a = a
        self.b = b
        self.range = range
    def __call__(self, a, b):
        self.a = a
        self.b = b
        print('__call__ with （{}, {}）'.format(self.a, self.b))
    def __del__(self, a, b, range):
        del self.a
        del self.b
        del self.range

xInstance = X(1, 2, 3)
xInstance(1,2)

#执行结果：__call__ with (1, 2)


class Animal(object):
    def __call__(self, words):
        print("Hello: ", words)


cat = Animal()
cat(words='word')