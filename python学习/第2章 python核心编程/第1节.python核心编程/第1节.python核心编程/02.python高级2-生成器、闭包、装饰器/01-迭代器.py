#-*- coding:utf-8 -*-
#author:YJ沛

'''
生成器一定是迭代器，迭代器不一定是生成器

列表不是迭代对象，但可以迭代

'''


#判断一个对象是否可迭代的方法：
from collections import Iterable

#判断字符串
print(isinstance("abcd",Iterable))  #True表示可迭代对象，否则不能

#判断字列表，字典，元组，数字等
print(isinstance([1,2,3],Iterable))     #True
print(isinstance([],Iterable))          #True
print(isinstance({},Iterable))          #True
print(isinstance((),Iterable))          #True
print(isinstance(100,Iterable))         #False

