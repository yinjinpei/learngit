#_*_ coding:utf-8 _*_

name_info = {'name':'peter','age':17,'name':'alex'}     #键重要时，前值会被后值替换

print(name_info)               #方法一，返回所有键和值，以列表形式输出

for i in name_info:            #方法二，读出字典键和值，效率高
    print(i,name_info[i])

for x,y in name_info.items():  #方法三，读出字典键和值, 效率低
    print('-----------------')
    print(x,y)

print(name_info.keys())        #返回所有键
print(name_info.values())      #返回所有值

name_info = {                  #定义字典
    'name':'peter',
    'age':17,
    'work':'IT',
    'wage':15000
}
print(str(name_info)+ '---str(dict），输出字典，以可打印的字符串表示。')
len(name_info)                 #计算元素个数，即键的总数
print(type(name_info))         #返回输入的变量类型，如果变量是字典就返回字典类型


name_info['sex'] = 'man'        #新增一个值
print(name_info)
print(name_info.setdefault('name',123))  #新增一个值,如何键已存在则不修改

name_info = {'name':'peter', 'age':17,'work':'IT', 'wage':15000 }
print(name_info.get('job',1))   #返回指定键，在则返回值，如果键不在字典中返回default值,可指定返回值
print('fuck' in name_info)      ##如果键在字典里返回true，否则返回false

print(name_info.pop('work'))    #方法一，指定删除某个值
#del name_info['work']          #方法二，指定删除某个值

#print(name_info.popitem())     #随机返回并删除字典中的一对键和值(一般删除末尾对)。

print(name_info.pop('all',1))   #删除一个值，如果不存在侧返回自定义的值

name_info = {'name':'peter', 'age':17,'work':'IT', 'wage':15000 }
name_info.clear()               #清空字典
print('#清空字典 %s ' % name_info)

#====================  浅度复制  ===========================

name_info = {'name':'peter', 'age':17,'work':'IT', 'wage':15000 }
dict_1 = name_info.copy()       #父对象进行了深拷贝，不会随name_info修改而修改
dict_2 = name_info              #子对象是浅拷贝,所以随-ame_info的修改而修改，相当于起别名为：dict_2

name_info.pop('work')       #实例
print(dict_1)
print(dict_2)
print('name' in dict_1)     #如果键在字典里返回true，否则返回false
print(name_info.items())    #以列表返回可遍历的(键, 值) 元组数组

name_info = {'name':'peter', 'age':17,'work':'IT', 'wage':15000,'friend': ['peter', 'alex'] }
dict_3    = name_info.copy()
name_info['friend'].append('jinpei')    #字典name_info中friend列表中添加一个，dict_3也会发生改变，这就是浅度复制
print(name_info)
print(dict_3)
#==========================================================

#====================  深度复制  ===========================

import copy     #导入深度复制库
name_info = {'name':'peter', 'age':17,'work':'IT', 'wage':15000,'friend': ['peter', 'alex'] }
dict_4    = copy.deepcopy(name_info)    #深度复制
name_info['friend'].append('boby')
print(name_info)
print(dict_4)
dict_4['friend'][0] ='JINPEi'
print(dict_4)
#==========================================================


name_info   = {'name':'peter', 'age':17,'work':'IT', 'wage':15000,'friend': ['peter', 'alex'] }
name_info_2 = {'job':'kill','friend':'no_friend','age':18 }
name_info.update(name_info_2)       #把name_info_2合并到name_info，把新的替换旧的
print(name_info)


