
class Base:
    def base(self):
        print("------- Base --------")

class A(Base):
    def a(self):
        print("------- aaa --------")

class B(Base):
    def b(self):
        print("------- bbb --------")

class C(A,B):   #多继承
    def c(self):
        print("------- ccc --------")

c = C()
c.c()
c.a()
c.b()
c.base()
