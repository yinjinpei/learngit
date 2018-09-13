#!/usr/bin/env python
#_*_ coding:utf-8 _*_


'''
如果遇到编码问题：参考如下：
    fr = open(odlFolderName+"/"+name,'r',encoding='UTF-8')
    fw = open(newFolderName+"/"+name, "w",encoding='UTF-8')
'''
f = open('readline_file.txt','r')

for line in f.readlines():
    print(line.strip().split(':'))
