#_*_ coding:utf-8 _*_


name_info = {                  #定义字典
    'name':'peter',
    'age':17,
    'work':'IT',
    'wage':15000
}

for i in name_info:            #读出字典的值
    print(name_info[i])

name_info['sex'] = 'man'       #新增一个值
print(name_info)

name_info.pop('work')          #指定删除某个值
print(name_info)

name_info.popitem()            #随机删除某个值
print(name_info)


name_info.popitem()            #随机删除某个值
print(name_info)
