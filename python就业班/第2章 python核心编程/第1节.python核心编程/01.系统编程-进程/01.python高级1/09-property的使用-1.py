#-*- coding:utf-8 -*-
#author:YJ沛

print("################## 获取、修改私有属性方法一 #################")
class Num:
    def __init__(self):
        self.num = 100
        self.__num2 = 150

    def setNum(self,new_num):
        self.__num2 = new_num

    def getNum(self):
        return self.__num2


t = Num()
#print(t.num)
print(t.getNum())

t.setNum(20)
print(t.getNum())


print("################## 获取、修改私有属性方法二 #################")
class Money:
    def __init__(self):
        self.__money = 1000

    def getMoney(self):
        return self.__money

    def setMoney(self,new_money):
        self.__money = new_money

    money = property(getMoney,setMoney) #使外面可以直接调用私有属性

m = Money()
print(m.money)  #原有值，直接调用

m.money = 100   #修改后的值，相当调用setMoney()方法
print(m.money)  #直接赋值，相当调用getMoney()方法