class Dog:
    #属性

    #方法
    def eat(self):
        print("正在吃鸡腿...")

    def drink(self):
        print("正在喝牛奶。。。")

    def behavior(self):
        print("%s是一只狗，今年%d岁"%(self.name,self.age)) #获取属性

#定义对象
tom = Dog()
alex = Dog()

#添加属性
tom.name = "金毛"
tom.age = 12
tom.behavior()

alex.name = "哈仕奇"
alex.age = 10
alex.behavior()




