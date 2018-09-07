#-*- coding:utf-8 -*-
#author:YJ沛

#动态创建类，一般不这怎么用
def test(name):
    if name == "Test1":
        class Test1(object):
            def print_info(self):
                print('------ Test1 -----')
        return Test1

    elif name == "Test2":
        class Test2(object):
            def print_info(self):
                print('-------- Test2 --------')
        return Test2

t1 = test("Test1")
t2 = test("Test2")
t1.print_info("xxx")
t2.print_info("xxxx")


#type创建类:  添加属性
Preson = type("Preson",(),{"num":100})  #类名 = type（类名，父类(用元组表示)，属性）
p1 = Preson()
print(p1.num)


#type创建类:  添加一个方法
def print_info():   #先定义方法函数
    print('---------print_info ---------')

Preson2 = type("Preson2",(),{"print_info":print_info})    #创建类并添加方法
p2 = Preson2    #相当于p2 = Preson2(),  应该是3.65修改了版本才这样写
p2.print_info()


#type创建类: 继承父类
Peter = type("Peter",(Preson2,),{})
peter = Peter
peter.print_info()