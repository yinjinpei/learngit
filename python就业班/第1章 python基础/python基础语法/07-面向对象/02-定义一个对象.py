class Dog:
    #属性

    #方法
    def eat(self):
        print("正在吃鸡腿...")

    def drink(self):
        print("正在喝牛奶。。。")

    def behavior(self):
        print("%s是一只狗，今年%d岁"%(tom.name,tom.age)) #获取属性

#定义一个对象
tom = Dog()
tom.eat()
tom.drink()

#添加属性
tom.name="金毛"
tom.age=12
tom.behavior()





