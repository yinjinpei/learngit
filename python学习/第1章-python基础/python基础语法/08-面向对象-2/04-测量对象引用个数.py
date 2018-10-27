import sys

class Dog:
    pass

t1 = Dog()  #创建对象

sum = sys.getrefcount(t1) #获取Dog()对象个数
print(sum)

t2=t1   #复制t1对象
sum = sys.getrefcount(t1) #获取Dog()对象个数
print(sum)

del t2
sum = sys.getrefcount(t1) #获取Dog()对象个数
print(sum)



