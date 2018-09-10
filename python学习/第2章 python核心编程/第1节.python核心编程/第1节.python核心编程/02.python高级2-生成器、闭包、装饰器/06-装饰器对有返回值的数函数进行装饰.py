#-*- coding:utf-8 -*-
#author:YJ沛

print("######### 对有返回值的数函数进行装饰 #############")
def func(funcName):
    def func_in():
        print("----- 正在装饰 -----")
        result = funcName() #保存 返回来的"peter"
        return result   #把"peter"返回给17行处的调用
    return func_in

@func
def test():
    print("---- test1 -----")
    return "peter"

ret = test()
print("him name is %s"%ret)
