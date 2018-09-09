#-*- coding:utf-8 -*-
#author:YJ沛

'''
以下是针对python2，python3都一样，id地址不变
小整数池：[-5 - 256] 这些字数系统已创建好了，不会被垃圾回收
大整数池：只有被创建时才会创建，可以被垃圾回收
intern机制：字符串共用一份，id地址一样

'''
#小整数池：[-5 - 256]
a = 100
b = 100
print(id(a))
print(id(b))

del a   #回收
del b

a1 = 100
b1 = 100
print(id(a1))   #结果和上面一样，同一地址，说明没有被回收掉
print(id(b1))


#大整数池
c = 10000
d = 10000
print(id(c))
print(id(d))

del c   #回收
del d

c1 = 10000
d1 = 10000
print(id(c1))   #结果和上面不一样，不同的地址，说明被回收掉了
print(id(d1))


#intern机制，字符串共用一份，id地址一样，如:
a = 'peter'
b = 'peter'
print(id(a))
print(id(b))

del a
del b
c = 'peter'
print(id(c))    #都一样?  可能是同一进程（同一程序），没有被回收掉？


