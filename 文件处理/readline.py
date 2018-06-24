#!/usr/bin/env python
#_*_ coding:utf-8 _*_


f = open("readline_file.txt",'r')
while True:
    line = f.readlines()      #对应内容一
    #line = f.readline()      #对应内容二
    if line:
        print('内容如下：')

        #内容一 ，与readlines使用
        data = line[1]
        print(data.strip())
        print(data.split(':')[0])
        print(data.split(':')[1].strip())   #split() 设置分割符    ;strip() 去空行
        print(data.strip('\n').split(':'))  #strip('\n') 去除换行符

        #内容二 ，与readline使用
        #print(line.strip().split(':')[0])
        #print(line.strip().split(':'))

        pass
    else:
        break
print('结束')
f.close()
