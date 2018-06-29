#!/usr/bin/env python
#_*_ coding:utf-8 _*_

f = open('peter_lock.txt','r')
data = f.read() #读出所有的内容
print(data)
f.close()