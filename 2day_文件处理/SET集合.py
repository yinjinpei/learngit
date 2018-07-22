#_*_ coding:utf-8 _*_

set_list = { 1,2,3,4,5,6 }  #初始化集合
set_list.add(7)             #添加一个数字
set_list.update( { 8,9 } )        #添加多个数字
set_list.update(['peter','alex'])   #添加列表

print(type(set_list))       #查看类型
print(set_list)             #查看集合

for i in set_list:          #查看集合,方法二
    print(i)
     

a = {1,2,3,4}
b = {3,4,5,6}
print( a & b )      #交集
print( a | b )      #并集
print( a - b )      #差值，结果为1，2
print( a ^ b )      #对称差值，结果为1，2，5，6

print(a.issubset(b))    #a是b的子集, b是否包含a
print(a.issuperset(b))  #a是否包含b