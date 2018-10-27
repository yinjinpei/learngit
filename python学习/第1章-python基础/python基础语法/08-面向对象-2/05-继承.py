
#定义动物（狗和猫）通用的类
class Animal:
    def __init__(self,new_name):
        self.name = new_name
        print(self.name)
    def eat(self):
        print("--------- 吃吃吃 Animal---------")
    def drink(self):
        print("--------- 喝喝喝 Animal---------")
    def run(self):
        print("--------- 跑跑跑 Animal---------")

class Dog(Animal):  #狗继承了动物类
    def call(self):
        print("--------- 汪汪汪 Dog------------")
class Cat(Animal):  #猫继承了动物类
    def cat_call(self):
        print("--------- 喵喵喵 Cat------------")

class BlackDog(Dog):    #即继承了狗类又继承了动物类
    def catch(self):
        print("--------- 捉坏人 BlackDog-------")

a = Animal("动物")
a.eat()

dog = Dog("小白狗")
dog.drink()

cat = Cat("汤姆猫")
cat.run()

blackDog = BlackDog("黑狗")
blackDog.run()
blackDog.call()
blackDog.catch()
