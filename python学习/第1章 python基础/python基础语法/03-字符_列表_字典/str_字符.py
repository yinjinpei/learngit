#_*_ coding:utf-8 _*_

name="peter"
for str in name:
    print(str,end="")
print("")

#取第三个元素
print(name[2])

#取最后一个元素,方法一：
print(name[-1])

#取最后一个元素,方法二：
lastNumber = len(name) - 1  #len()获取总长度
print(name[lastNumber])


#切片
name = "peterABCDEF"
#取2到4，包括4
print(name[2:5])

#取2到倒数第二个,即t到E
print(name[2:-1])

#取2到最后
print(name[2:])

#从2取到8，但每隔2个步长取,即trBD
print(name[2:9:2])

#对name字符串逆序打印
print(name[::-1])

#总结：格式：name[起始位置:终止位置-1:步长]  #步长为正数
#总结：格式：name[终止位置-1:起始位置:步长]  #步长为负数



print('------------------------------------------')
temp = ['@所有人','@all','@aLL','@alL','@aLl','@All','@ALL','@ALl','@AlL']

for i in temp:
    print(i.upper())

num = input("num :")
print(type(num))