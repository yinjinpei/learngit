#!/usr/bin/env python
#_*_ coding:utf-8 _*_

f = open('write_passwdFile.txt','r')
#print(f.readline())
#f.seek(0)
#读取文件前三个用户名
a = 1
while a < 4:
    print(f.readline().split(':')[0])
    a += 1
f.close()


f = open("write_file.txt",'w')
f.write('hihi')     #以覆盖形式写入
f.write('sksk')
f.write('\nggggsssg')  #\n 表示换行后再写入
f.close()