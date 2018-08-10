#_*_ coding:utf-8 _*_

#####################  三元运算 ###################
#普通运算
temp = None
a = 3
b = 1
if a > b:
    temp = '成立'
else:
    temp = '不成立'
print(temp)

#三元运算
a = 3
b = 1
result = '成立' if a > b else '不成立'
print(result)

#####################  lambda运算 ###################

temp = lambda a,b:a+b
print(temp(3,5))

temp = lambda x:x*x
print(temp(6))

temp = lambda x,y,z:x+y*z
print(temp(1,2,3))

list=[x*2 for x in range(10)]
print(list)

map(lambda x:x*2,range(10))

l2=map(lambda x,y:x**y,[1,2,3],[1,2,3])
for i  in l2:
    print(i)

#python3中可以处理类表长度不一致的情况，但无法处理类型不一致的情况，
l4=map(lambda x,y:(x**y,x+y),[1,2,3],[1,2])
for i in l4:
    print(i)

#特殊用法，做类型转换：
l=map(int,'1234')
for i in l:
    print(type(i))
    print(i)

