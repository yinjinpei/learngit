#-*- coding:utf-8 -*-

a={"age":1,"name":"peter"}

def print_sum(a,b,*args,**kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)

print_sum(1,2,3,4,a,name="jinpei")


print("="*50)
#拆包
A=(22,"bb")
B={"age":1,"name":"peter"}


def print_sum(a,b,*args,**kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)

print_sum(11,22,*A,**B) #拆包传字典和元组

