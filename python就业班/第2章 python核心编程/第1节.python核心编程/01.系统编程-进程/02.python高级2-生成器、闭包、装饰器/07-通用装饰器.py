#-*- coding:utf-8 -*-
#author:YJ沛

print("######### 通用装饰器 #############")

def func(funcName):
    def func_in(*args,**kwargs):
        result = funcName(*args,**kwargs)
        return result
    return func_in

@func
def test(a,b,c,d):
    print("---- test1 -----")
    print("a=%s,b=%s,c=%s,d=%s"%(a,b,c,d))
    return "peter",a,b,c,d

@func
def test2(a,b):
    print("----- test2 ----- ")




ret = list(test("asd3",6,2343456,3))
print("him name is %s"%ret[0])
print(ret)


a = test2(11,22)
print(a)