

class Dog(object):
    __instance = None   #用来储存创建的对象的引用
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance   #返回上次创建的对象的引用

    def __init__(self,new_name):
        if self.__first_init:
            self.name = new_name
            self.__class__.__first_init = False
        # 或者：
        # if Dog.__first_init:
        #     self.name = new_name
        #     Dog.__first_init = False

a=Dog("金毛")
print(id(a))
print(a.name)

b=Dog("中华田园犬")
print(id(b))
print(b.name)