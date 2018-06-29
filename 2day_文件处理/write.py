#!/usr/bin/env python
#_*_ coding:utf-8 _*_


f = open('write_passwdFile.txt','r')
for i in f.readlines():
    print(i)
f.close()

f = open("write_file.txt",'w')
f.write('hihi')     #以覆盖形式写入
f.write('sksk')
f.write('\nggggg')  #\n 表示换行后再写入
f.close()
