#!/usr/bin/env python
#_*_ coding:utf-8 _*_

name_list = ['peter','jinpei','xiaoming','peter']

name_list.append('huge')          #追加一个元素
print(name_list)

name_list.insert(1,'zhaoliying')  #在第1个元素前面插入元素
print(name_list)

print('------------删除单个或重复元素 如下-----------')
name_list = ['peter','jinpei','xiaoming','peter']
name_list.remove('peter')         #删除单个元素
print(name_list)

name_list   = ['peter','jinpei','xiaoming','peter']
name_list_1 = list(set(name_list)) #删除重复元素，只保留一个
print('删除重复：',name_list_1 )

print('------------按元素索引位置删除元素 如下-----------')
name_list = ['peter','jinpei','xiaoming','peter']
del name_list[0]                 #按元素索引位置删除
print(name_list)

name_list = ['peter','jinpei','xiaoming']
print(name_list.pop())           #删除列表最后一个，并打印删除的元素
print(name_list)
print(name_list.pop(1))          #按元素索引位置删除，并打印删除的元素
print(name_list)

print('-------------统计重复元素的次数 如下----------')

name_list = ['peter','jinpei','xiaoming','peter']
print(name_list.count('peter'))  #统计列表中‘peter’出现的次数

print(name_list.index('peter'))  #元素索引位置
print(name_list)

print('-------------数组元素反向排列 如下----------')
name_list = ['1','2','3','4']
print(name_list)
name_list.reverse()              #数组元素反向排列
print(name_list)

print('-------------按ASCII小到大排列 如下----------')
name_list = ['11','2','34','24']
print(name_list)
name_list.sort()
print(name_list)                 #按ASCII小到大排列，注意判断的是第1位

print('-------------列表相加 如下----------')
name_list = ['peter','jinpei','xiaoming','peter']
infos = [1,2,4,5,6,7,8]

name_list.extend(infos)         #方法一： 列表相加
print(name_list)

name_list = ['peter','jinpei','xiaoming','peter']
name_list += infos               #方法二： 列表相加
print(name_list)

print('-------------列表中元素对应相加，即索引相同的组合 如下----------')
import itertools
a,b=[1,2,3],[4,5,6]
c = list(itertools.product(a,b))

print('-------------列表中元素对应相减，即索引相同的相减 如下----------')
v1 = [21, 34, 45]
v2 = [55, 25, 77]
v = list(map(lambda x: x[0]-x[1], zip(v2, v1)))
print("%s\n%s\n%s" %(v1, v2, v))


print('-------------取列表中某段元素 如下----------')
char = ['peter','jinpei','xiaoming','peter','1','2','3','4']
print(char[2:6])   #取第2，3，4，5位置元素，注意：最后一位不取，即顾前不顾后
print(char[-5:])   #取最后5位元素
print(char[-5:-1])

print('-------------实例 如下----------')
#实例:从peter位置往后取3个值，包含peter，一共4个元素
char = ['jinpei','xiaoming','peter','1','2','3','4','5']
print(char[char.index('peter'):char.index('peter')+4])

print('-------------找出数组中‘peter’的所有索引位置，如下----------')
name  = ['jinpei','xiaoming','peter','1','2','3','peter','4','5','peter','ddd','peter','hhh','peter']
char = 'peter'                          #定义要找的元素名称：peter
first_pos = 0
for i in range(name.count(char)):
        new_list = name[first_pos:]
        next_pos = new_list.index(char) + 1
        print('找到了：',new_list.index(char) + first_pos)
        first_pos += next_pos


print('-------------自定义隔几个数取值，如下----------')
name  = ['jinpei','xiaoming','peter1','1','2','3','peter2','4','5','peter3','ddd','peter','hhh','peter']
print(name[1::2])      #隔1个取值，左边的1表示：从索引1位置开始，右边的2表示隔2个元素取值
print(name[2::4])      #隔2个取值，左边的2表示：从索引2位置开始，右边的4表示隔4个元素取值