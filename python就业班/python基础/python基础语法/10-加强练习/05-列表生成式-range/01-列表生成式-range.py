#把包括10-30之间的数字写到a列表中

#方法一:
i = 10
a = []
while i <=30:
    a.append(i)
    i += 1
print(a)

#方法二:
#表达式一：
a = []
for i in range(10,31):
    a.append(i)
print(a)

#表达式二:
a = [i for i in range(10,31)]
print(a)


#把包括0-30之间的偶数写到a列表中
#方法一：
a = [i for i in range(0,30,2)]
print(a)

#方法二:
a = [i for i in range(0,30) if i%2==0]
print(a)



#其他用法
a = [(i,j) for i in range(3) for j in range(2)]     #前for循环1次，后for循环2次所以，一共6次
print(a)


#其他用法
a = [(i,j,k) for i in range(3) for j in range(2) for k in range(2)]
print(a)