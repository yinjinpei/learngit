#!user/bin/env python
#_*_ coding:utf-8 _*_


name = input('请输入我的名字:')

age = 40
for i in range(10):
    while True:
        try:
            age = int(input('猜下我的年龄？:'))
            break
        except ValueError:
            print('输入错误，输入内容必须为正整数数字，请重新输入：')
    if  age > 40 and i < 9:
        print('你输入的数字比正确的要大!!')
    elif age > 0 and i == 9:
        print('一共可猜10次，已积累猜答次数：%s' % (i + 1), '你没有机会了！！！')
        break
    elif age == 40 and i < 9:
        print('\033[1;32;41m 真聪明，恭喜你，猜对了！！！\033[0m')
        break
    elif age < 40 and i < 9:
        print('你输入的数字比正确的要小！！')
    else:
        print('输入异常！！')

    print('一共可猜10次，已积累猜答次数：%s' % (i + 1))
    print('你还有 %s 机会, 请重新输入: ' % (9 - i))

print ('''
Personal information of %s:
        Name: %s
        Age:  %s   

--------------------------
      
''' % (name,name,age))

