#!/usr/bin/python3
# _*_ coding:utf-8 _*_
#字符串处理


msg = "what are your name,Peter,joke?"
b = 'a'

num = msg.find(b)   #find() 是从字符串左边开始查询子字符串匹配到的第一个索引
print(num)

num_1 = msg.rfind(b)    #rfind()是从字符串右边开始查询字符串匹配到的第一个索引
print(num_1)

print(msg.index(b))     #找到会返回值，找不到会报错

print(msg.capitalize()) #将首字母自动变成大写，其余变成小写

print(msg.upper())      #将所有字母都转成大写

print(msg.lower())      #将所有字母都转成小写

print(msg.swapcase())   #大小写互换

print(msg.split(','))   #字符串变成列表
print('|'.join(msg.split(',')))     #把列表中的元素以'|'连接起来,与split相反
#实用例子
char = ['p','e','t','e','r']
char_2 = ['is','good','boy!']
print(''.join(char) + ' ' + ' '.join(char_2))

x = 'Abc'
print(x.startswith('Ac'))   #判断以‘A’开头匹配，正确返true, 否则返false
print(x.startswith('Ab'))
print(x.startswith('Abcy'))
print('----------------')
print(x.endswith('c'))      #判断以‘c’结尾匹配，正确返true, 否则返false
print(x.endswith('bc'))
print(x.endswith('Abcy'))

