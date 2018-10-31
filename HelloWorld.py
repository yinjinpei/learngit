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



class A:
    def test(self,a,b):
        c=a+b
        print("-----------",c)

    def test2(self):
        b.test3(self.test)


class B:
    def test3(self,fun):
        a=1
        b=2
        fun(a,b)
aa= A()
b = B()
aa.test2()


for i in range(10):
    if i == 5:
        print ('found it! i = %s' % i)
        break
else:
    print( 'not found it ...')


