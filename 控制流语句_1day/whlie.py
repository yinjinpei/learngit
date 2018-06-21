#!/usr/bin/env python
#_*_ coding:utf-8 _*_


count = 0
while True:
    try:
        print_num = int(input('请输入一个数字： '))
        break
    except ValueError:
        print('输入错误，请输入一个正整数!!')

while count < 1000000:
    if count == print_num:
        print('两个数字相等！！', '数字为：', count)
        str_1 = input('是否继续输入？ Y/N :   ')
        #print(type(str_1))

        if str_1 == 'y':
            #print('继续输入！！！')
            while True:
                try:
                    print_num = int(input('请输入一个数字： '))
                    if print_num < count:
                        print('请输入一个比' ,count, '大的数字！！')
                        continue
                    break
                except ValueError:
                    print('输入错误，请输入一个正整数!!')
        else:
            print('结束输入！！！')
            break
    else:
        count += 1
        print(count)