# coding:utf-8
# author:YJ沛


'''
单向链表：只能单方向，有数据区和，指向地址区
'''


# 1，定义节点
class Node(object):
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class A(object):
    def __init__(self, a=None):
        self.__a=a

    def b(self):
        return self.__a == None

c = A(100)
print(c.b())