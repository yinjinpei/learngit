

class Dog(object):

    def __init__(self):
        print("----init方法----")

    def __del__(self):
        print("----del方法----")

    def __str__(self):
        print("----str方法----")

    def __new__(cls):   #cl此时是Dog指向的那个类对象
        print("----new方法----")
        return object.__new__(cls)



dog=Dog()
#1，调用 __new__()方法来创建对象，然后找一个变量来接收__new__的返回值，这个返回值表示创建出来的对象的引用
#2，__init__() 刚刚创建出来的对象的应用
#3，返回对象的引用