#-*- coding:utf-8 -*-
#author:YJ沛

print("################## 获取、修改私有属性方法三 #################")
class Money:
    def __init__(self):
        self.__money = 1000
        self.__num = 200

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self,new_money):
        self.__money = new_money


    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self,new_num):
        self.__num = new_num



m = Money()
m.money = 2000
print(m.money)

print("----------------------")
print(m.num)
m.num = 20000
print(m.num)