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