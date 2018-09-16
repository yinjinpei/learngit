#-*- coding:utf-8 -*-
#author:YJ沛


class Person(object):
    def __init__(self,newName,newAge):
        self.name = newName
        self.age = newAge

    def eat(aa):
        print("------- %s 在吃饭 --------"%aa.name)


alex = Person("alex",22)
print(alex.name);print(alex.age);alex.eat()

peter = Person("peter",18)
print(peter.name);print(peter.age);peter.eat()

#添加peter对象属性，只能给peter对象用，其他对象用不了
peter.addr = "深圳"
print(peter.addr)

#添加类属性,所有对象都可以用
Person.job = "IT"
print(alex.job)
print(peter.job)
