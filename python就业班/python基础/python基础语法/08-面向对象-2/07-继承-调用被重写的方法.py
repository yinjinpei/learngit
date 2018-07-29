

#定义狗通用的类
class Dog():
    def call(self):
        print("--------- 汪汪汪 Dog---------")
    def eat(self):
        print("--------- 吃吃吃 Dog---------")
    def drink(self):
        print("--------- 喝喝喝 Dog---------")
    def run(self):
        print("--------- 跑跑跑 Dog---------")

class BlackDog(Dog):    #即继承了狗类
    #重写方法，不用继承run()方法
    def run(self):
        print("--------- 疯狂跑 BlackDog----")

        #第1种，调用被重写的方法
        Dog.run(self)

        #第2种
        super().run()


blackDog = BlackDog()
blackDog.run()  #使用重写的方法
