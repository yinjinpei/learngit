#-*- coding:utf-8 -*-
#author:YJ沛

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
