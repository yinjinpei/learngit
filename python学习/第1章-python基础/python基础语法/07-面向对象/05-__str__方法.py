class Dog:

    def __init__(self,newName,newAge):
        #相当于在类内的全局变量
        self.name = newName
        self.age = newAge

    def __str__(self):
        return "%s的年龄是:%d" % (self.name, self.age)

    #方法
    def eat(self):
        print("正在吃鸡腿...")
    def drink(self):
        print("正在喝牛奶。。。")

#定义对象
tom = Dog("金毛",15)
alex = Dog("哈仕奇",11)

print(tom)
print(alex)




