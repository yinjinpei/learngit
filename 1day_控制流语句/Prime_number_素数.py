#_*_ coding:utf-8 _*_
#求 1 至 100 的质数

# -*- coding: UTF-8 -*-


'''
n = int(input('请输入一个数字'))

number = 1
while number < n:
    number += 1
    for i in range(2,number):
        z =  number % i
        if z == 0:
            print('这不是一个质数（素数）：%s' % number)
            break
    else:
         print('这是一个质数（素数）：%s' % number)
'''

y = 1   #初始化要判断的数字
while y < 100:
    y +=1
    x = 1   #初始除数
    for x in range(2,y):
        if not (y%x):   #当(y%x)等于0时，为false,前面加not表示为true
            print('这不是一个质数：%s' % y )
            break
    else:
        print('-------这是一个质数： %s' % y)