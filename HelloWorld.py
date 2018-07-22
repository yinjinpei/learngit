import itertools
print('hello world!')


print(ord('~'))
print(ord('b'))

print('-------------列表中元素对应相加，即索引相同的组合 如下----------')

a,b=[1,2,3],[4,5,6]
c = list(itertools.product(a,b))
print(c)


'''print('-------------列表相加 如下----------')

a = ['a','b','c','d','e','f','g']
b = [1,2.3,4.5,6,7]

char = a[0] + b[1][0]
print(char)


'''