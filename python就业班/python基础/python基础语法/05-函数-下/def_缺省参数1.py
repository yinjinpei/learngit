#-*- coding:utf-8 -*-

def print_info(a,b,c=1):    #c为缺省参数，默认取1
    result=a+b+c
    print("%d+%d+%d=%d"%(a,b,c,result))

#print_info(11,22,33)
#print_info(1,2)

def print_sum(a,b,*args):
    sum_test = 0
    for i in args:
        sum_test = sum_test +i
    print(sum_test + a + b)
    return sum_test

print_sum(1,2,3,4)
sum_test2=print_sum(11,22,33,44)
print(sum_test2)