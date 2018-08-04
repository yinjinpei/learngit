
class CarStore(object):
    def order(self,car_type):
        return Factory(car_type)

def Factory(car_type):          #解耦 单独从CarStory()中分离出来，以后新增车型号不用修改CarStore()类
    if car_type == "玛莎拉帝X1":
        return Maserati_X1()
    elif car_type == "玛莎拉帝X2":
        return Maserati_X2()
    elif car_type == "玛莎拉帝X3":
        return Maserati_X3()


class Car(object):
    def move(self):
        print("飚车中。。。")
    def music(self):
        print("听音乐。。。")
    def stop(self):
        print("急刹车。。。")

class Maserati_X1(Car):
    def print_info(self):
        print("玛莎拉帝X1")

class Maserati_X2(Car):
    def print_info(self):
        print("玛莎拉帝X2")

class Maserati_X3(Car):
    def print_info(self):
        print("玛莎拉帝X3")

carstore = CarStore()
car = carstore.order("玛莎拉帝X2")
car.print_info()
car.move()
car.music()
car.stop()

