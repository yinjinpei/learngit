#!/usr/bin/env python
#_*_ coding:utf-8 _*_

f = open('readline_file.txt','r')

for line in f.readlines():
    print(line.strip().split(':'))
