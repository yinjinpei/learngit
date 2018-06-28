#_*_ coding:utf-8 _*_

set_list = { 1,2,3,4,5,6 }  #初始化集合
print(type(set_list))       #查看类型
print(set_list)             #查看集合

for i in set_list:          #查看集合,方法二
    print(i)

a = {1,2,3,4}
b = {3,4,5,6}
print( a & b )      #交集
print( a | b )      #并集
print( a - b )      #差值，结果为1，2
print( a ^ b )      #反差值
