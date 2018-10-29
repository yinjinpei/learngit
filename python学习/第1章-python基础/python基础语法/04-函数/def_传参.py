#-*- coding:utf-8 -*-

################ 单个传参 ################

def temperature():
    number=22
    print(number)
    return number

def trun_temperature(number):
    number*=10
    print(number)

result=temperature()
trun_temperature(result)

################ 多个传参 ###################

def test():
    a=11
    b=12
    c=13

    d =[a,b,c]
    e ={a,b,c}
    #方法一，以元组方式
    return a,b,c    #等同于 return (a,b,c)

    #方法二，以列表方式
    #return d  #等同于return [a.b,c]

    #方法三，以字典方式
    #return e   #等同于return {a.b,c}


def test_2(a,b,c):
    d = a+b+c
    return d

result = test()
print(result)
print(test_2(
    result[0],result[2],result[1]))
