#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import sys,os


#fileName = input('请输入需要替换的文件名：')
#oldValue = input('请输入旧的内容：')
#newValue = input('请输入新的内容：')

old_char = sys.argv[1]
new_char = sys.argv[2]
fileName = sys.argv[3]

old_file = open(fileName,'r')
new_file = open('.%s.bak' % fileName,'w+')

for line in old_file.readlines():
    new_file.write(line.replace(old_char,new_char))

old_file.close()

############# 可去除部分，至下 ############
new_file = open('.%s.bak' % fileName,'r+')
while True:
    line = new_file.readline()
    if line:
        print('内容如下：%s' % line.strip())
        pass
    else:
        break
############# 可去除部分 至上 ############
new_file.close()

if '--bak' in sys.argv:     #判断'--bak'是否有
    os.rename(fileName,fileName+'.bak')
    os.rename('.%s.bak' % fileName, fileName)
else:
    os.remove(fileName)
    os.rename('.%s.bak' % fileName, fileName)



