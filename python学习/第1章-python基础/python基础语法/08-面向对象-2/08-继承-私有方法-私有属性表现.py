
class A:
    def __init__(self):
        self.name = "peter"
        self.__age = 18
    def test1(self):
        print("----- test1 %s------"% self.name)
        print("----- test1 %d------"% self.__age)

    def __test2(self):
        print("----- test2 %s------"% self.name)
        print("----- test2 %d------"% self.__age)

class B(A):
    def bb(self):
        print(self.name)
        #print(self.__age)  #私有属性不会被继承，报错："AttributeError: 'B' object has no attribute '__age'"
        #self.__test2()     #私有方法不会被继承，报错：“AttributeError: 'B' object has no attribute '_B__test2'”
        self.test1()        #证明在父类中，公有属性可以调用私有属性反回给子类

t1 = B()
print(t1.name)     #获取公有属性
#print(t1.__age)   #获取私有属性 ，会报错，获取不到: "AttributeError: 'B' object has no attribute '__age'"
t1.bb()            #证明在父类中，公有属性可以调用私有属性反回给子类
#t1.__test2()      #私有方法不会被继承，报错：“AttributeError: 'B' object has no attribute '_B__test2'”