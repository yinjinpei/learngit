#_*_ coding:utf-8 _*_
#打印偶数

'''
#打印1-100中的偶数：
frequency = 1
while frequency <= 50:
    print(frequency*2)
    frequency +=1
'''

#打印1-100中前20个的偶数,：
frequency = 1
flag = 0
while frequency <= 100:

    if frequency%2 == 0:
        print(frequency)
        flag +=1

    if flag == 20:
        break
    frequency +=1