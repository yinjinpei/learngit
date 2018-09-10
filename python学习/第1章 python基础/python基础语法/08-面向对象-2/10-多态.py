
class A(object):    #object，可写可不写，默认是继承这个
    def print_self(self):
        print("-------- a ----------")

class B(object):
    def print_self(self):
        print("-------- b ----------")

def C(name):
    name.print_self()
    print("-------- c ----------")

test = A()
C(test)
print("")

test1 = B()
C(test1)

#面试题：面向对象三个基本要素？        答：封装，继承，多态
#       python是面向过程还是面向对象？答：即是面向过程又是面向对象