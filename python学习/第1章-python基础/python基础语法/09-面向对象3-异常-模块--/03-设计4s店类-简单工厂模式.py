
class Store(object):
    def select_car(self,car_type):
        pass

    def order(self,car_type):
        return self.select_car(car_type)

class CarStore(Store):
    def select_car(self,car_type):
        return Factory().select_car_by_type(car_type)

class BMWCarStore(Store):          #新增奔驰类型
    def select_car(self,car_type):
        return BMWFactory().select_car_by_type(car_type)


class Factory(object):
    def select_car_by_type(self,car_type):          #解耦 单独从CarStory()中分离出来，以后新增车型号不用修改CarStore()类
        if car_type == "玛莎拉帝X1":
            return Maserati_X1()
        elif car_type == "玛莎拉帝X2":
            return Maserati_X2()
        elif car_type == "玛莎拉帝X3":
            return Maserati_X3()

class BMWFactory(object):
    def select_car_by_type(self,car_type):
        if car_type == "奔驰X5":
            return Mercedes_X5()
        elif car_type == "奔驰X6":
            return Mercedes_X6()
        elif car_type == "奔驰X7":
            return Mercedes_X7()


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

class Mercedes_X5(Car):
    def print_info(self):
        print("奔驰X5")

class Mercedes_X6(Car):
    def print_info(self):
        print("奔驰X6")

class Mercedes_X7(Car):
    def print_info(self):
        print("奔驰X7")

carstore = CarStore()
car = carstore.order("玛莎拉帝X2")
car.print_info()
car.move()
car.music()
car.stop()

print("")

bmw_storecar = BMWCarStore()
bmw = bmw_storecar.order("奔驰X7")
bmw.print_info()
bmw.move()
bmw.music()
bmw.stop()


