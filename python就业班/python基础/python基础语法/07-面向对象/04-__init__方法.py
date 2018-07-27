class Dog:

    def __init__(self,newName,newAge):
        self.name = newName
        self.age = newAge

    #方法
    def eat(self):
        print("正在吃鸡腿...")
    def drink(self):
        print("正在喝牛奶。。。")
    def behavior(self):
        print("%s是一只狗，今年%d岁"%(self.name,self.age)) #获取属性

#定义对象
tom = Dog("金毛",15)
alex = Dog("哈仕奇",11)
tom.behavior()
alex.behavior()




