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



'''
集合特点：没有重复值，没有顺序
'''

a = {'a','b','c','d','e','f','g'}
b ={'b','c','d','f','h','x'}

#交集
print(a&b)  #执行结果：{'d', 'f', 'c', 'b'}


#并集
print(a|b)  #执行结果：{'f', 'c', 'b', 'x', 'd', 'a', 'h', 'g', 'e'}


#差值
print(a-b)  #执行结果：{'a', 'g', 'e'}   相当于a减去a和b交集


#对称差值
print(a^b)  #执行结果：{'a', 'h', 'x', 'g', 'e'} 除了a和b交集之外的单独所有元素的集合