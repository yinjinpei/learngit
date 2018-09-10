#-*- coding:utf-8 -*-
#author:YJ沛

print("######### 对无参数的函数进行装饰 #############")
def func(funcName):
    def func_in():
        print("----- 正在装饰 -----")
        funcName()
    return func_in

@func
def test():
    print("---- test1 -----")

test()

print("########### 对有参数的函数进行装饰 #############")
def func_1(funcName):
    def func_in(a,b):   #如果a,b 没有定义形参，那么会导致test_1(a,b)函数调用失败
        print("----- 正在装饰 -----")
        funcName(a,b)   #如果没有把a,b当做实参进行传递，那么会导致调用test_1(a,b)函数调用失败
    return func_in

@func_1 #test_1 = func_1(test_1(a,b))
def test_1(a,b):
    print("---- test1_1 -----")
    print("a=%d,b=%d"%(a,b))
test_1(11,22)


print("########### 对不定长参数的函数进行装饰 #############")
def func_2(funcName):
    def func_in(*args,**kwargs):
        print("----- 正在装饰 -----")
        funcName(*args,**kwargs)
    return func_in

@func_2
def test_2(*args,**kwargs):
    print("---- test1_2 -----")
    print(*args,**kwargs)   #拆包后的显示
    print(args, kwargs)     #不拆包的显示
test_2(11,22,123,24,23,43,534,645,67,"dasdfasdf")
