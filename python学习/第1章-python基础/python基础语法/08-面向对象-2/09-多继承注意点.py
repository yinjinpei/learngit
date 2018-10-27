
'''所有类中方法名字都相同'''
class Base:
    def test(self):
        print("------- Base --------")

class A(Base):
    #def test(self):    #蔽屏3
    #    print("------- aaa --------")
    pass

class B(Base):
    #def test(self):    #蔽屏2
    #    print("------- bbb --------")
    pass

class C(A,B):   #多继承
    #def test(self):    #蔽屏1
    #    print("------- ccc --------")
    pass

c = C()
c.test()

#类名.__mro__  获取调用父类方法的优先级，由C3算法决定
print(C.__mro__)
print(B.__mro__)
print(A.__mro__)
print(Base.__mro__)