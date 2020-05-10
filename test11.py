# coding:utf-8
# author:YJ沛

import re

text = 'uploads/peter/新建文件夹/constantly-15.1.0-py2.py3-none-any.whl'

patten = re.compile(r'.+?/')
result = patten.findall(text)

print(result)

up_one_level_path=''
for i in range(len(result)-1):
    up_one_level_path+=result[i]

print(up_one_level_path)


a=text.split('/')
print(a)
up_one_level_path=''
for i in range(len(a)-1):
    print(i)
    up_one_level_path+=a[i]+'/'



print(up_one_level_path[:-1])



a=10
b={}
for i in range(a):
    if i % 2 == 1:
        b[i] = 1
    else:
        b[i] = 0

print(b)



text = 'uploads/peter/新建文件夹/constantly-15.1.0-py2.py3-none-any.whl'
print(text[-1])
print(text[:-1])