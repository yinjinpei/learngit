#!/usr/bin/env python
#_*_ coding:utf-8 _*_
user_file = 'NameFile.txt'
info = input('Input the info to search: ')
f = open(user_file,'r')
count = 0
for line  in f.readlines():
    line = line.strip().split()
    #print(line)
    if info in line:
        print(line)
        line = ["\033[31m %s \033[0m" % info if i == info else i for i in line]
        for i in line:
            print(i)
        print('\n')
        count += 1
if count == 0:
    print('the info is not exists in your txt')
else:
    print('match %d lines'%(count))
f.close()