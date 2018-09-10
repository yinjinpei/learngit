#-*- coding:utf-8 -*-
#author:YJ沛

'''
__getattribute__:类属性访问拦截器,不能返回属性，不然会死循环.

'''
print("#################### range、xrang ####################")
range(1,1000)
#xrange(1,1000)  python2用的，和range有区别，xrange比较少空间

testList = [x*2 for x in range(5)]  #列表即时生成
testList = (x*2 for x in range(5))  #生成器，使用next()或__next__()或for获取值

print("#################### map 函数 ####################")
'''
map函数会根据提供的函数对指定序列做映射
'''
#map函数，传一个参数
a = map(lambda x:x*x,[1,2,3])
for i in a:
    print(i)
#或print(list(a))
#执行结果：1，4，9

#map函数，传二个参数
b = map(lambda x,y:x+y,[1,2,3],[5,6,7])
for i in b:
    print(i)
#执行结果：6，8，10

c = map(lambda x,y:x+y,['aa','bb','cc'],['dd'])
for i in c:
    print(i)
#执行结果：aadd


def test(x,y):
    return (x,y)

a = [1, 2, 3, 4, 5, 6, 7, 8]
b = ['a', 'b' ,'c' ,'d' ,'e' ,'f' ,'g' ,'h']
ret = map(test,a,b)
print(list(ret))
#执行结果：[(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e'), (6, 'f'), (7, 'g'), (8, 'h')]

print("#################### filter 函数 ####################")
'''
filter(...)
  --function:接受一个参数，返回布尔值True或False
  --sequence:序列可以是列表，元组，字符串
  
filter函数会对指定序列执行过滤操作。
filter函数对序列参数sequence中每个元素调用function函数，最后返回的结果包含调用结果为True的元素
'''

a = filter(lambda x:x%2, [1, 3, 4, 5, 6])   #除0为False，其它数字为True
print(list(a))
#执行结果：[1, 3, 5]

b = filter(None,['aa','bb','cc'])   #function参数为None，则返回所有结果
print(list(b))
#执行结果：['aa', 'bb', 'cc']


print("#################### reduce 函数 ####################")
'''
reduce（）的使用方法形如reduce(f(x),Itera).对，它的形式和map()函数一样。不过参数f（x）必须有两个参数。
reduce()函数作用是：把结果继续和序列的下一个元素做累积计算。
注意，第一个参数不能为None
'''
from functools import reduce    #导入模块

#reduce 函数传一个参数
a = reduce(lambda x,y:x+y, [1,2,3,4,5])     #此方式相当于计算总和
print(a)
#执行结果：15

#reduce 函数传两个参数
b = reduce(lambda x,y:x+y,[1, 2, 3, 4, 5, 6],8)
print(b)
#执行结果：29

c = reduce(lambda x,y:x+y, ['a','b','c','d'])     #此方式相当于计算总和
print(c)
#执行结果：abcd


print("#################### sorted 函数 ####################")
'''
sorted() 函数对所有可迭代的对象进行排序操作。

sort 与 sorted 区别：
sort 是应用在 list 上的方法，sorted 可以对所有可迭代的对象进行排序操作。
list 的 sort 方法返回的是对已经存在的列表进行操作，而内建函数 sorted 方法返回的是一个新的 list，而不是在原来的基础上进行的操作。

sorted 语法：
orted(iterable, key=None, reverse=False)  
    iterable -- 可迭代对象。
    key -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
    reverse -- 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。
'''

a = [2,31,2,1,61,31,651,31,854,3,1,684,3,6,5]
print(sorted(a))
print(sorted(a,reverse=True))
print(a)
