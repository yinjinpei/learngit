#!/usr/bin/env python
#_*_ coding:utf-8 _*_


#列表（list）表示方式
b = [1,2,3,4,5,6]
print(type(b))

#元组（tuple）表示方式，元组是常量数组，不可修改，需要修改可以先转成数组再修改，修改后再转成元组即可
a = (1.2,3,4,5,6)
print(type(a))
print(a)

print('--------- 元组转换成列表方法 ---------')
a_list  = list(a)           #转换成列表
print(type(a_list))
print(a_list)

a_tuple = tuple(a_list)     #转换成元组
print(type(a_tuple))
print(a_tuple)

