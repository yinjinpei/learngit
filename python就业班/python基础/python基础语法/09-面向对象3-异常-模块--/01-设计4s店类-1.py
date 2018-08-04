
class CarStore(object):
    def order(self,car_type):
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
car = carstore.order("玛莎拉帝X1")
car.print_info()
car.move()
car.music()
car.stop()

