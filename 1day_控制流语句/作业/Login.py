#!/usr/bin/env python
#_*_ coding:utf-8 _*_


'''
  编译登录接口
    1.输入用户名和密码
    2.认证成功后显示欢迎信息
    3.输错三次后锁定
------------------------------
使用方法:
    输入固定用户：peter
    正确密码：12345678 （密码可修改，修改peter_passwd.txt中的值即可）
        测试1：连续输入错误密码2次，然后输入一次正确密码，观察过程中peter_lock.txt中的值变化情况。
        测试2：连接输入错误密码4次，然后输入一次正确密码，观察过程中peter_lock.txt中的值变化情况。
'''


userName    = input('请输入你的用户名：  ')
userPasswd  = input('请输入你的密码：   ')
user_Passwd_TXT  = userName+'_passwd.txt'
f    = open(user_Passwd_TXT,'r')

#逐读取文件内容的每一行
while True:
    line = f.readline()
    if line:
        line_1 = line
        pass    #回到循环
    else:
        break
f.close()


#判断密码是否正确
if userPasswd == line_1:
    print('登录成功！！')
    #记录输入密码错误次数清零
    file  = open("peter_lock.txt",'w')
    file.write('0')
    file.close()

else:
    file     = open("peter_lock.txt",'r')
    lock_num = file.readline()
    file.close()

    unm_2 = int(lock_num)
#    print(unm_2)
#    print(type(unm_2))

    if unm_2 > 2:
        print('密码错误，因输入多次错误，帐号已被锁定，请联系管理员！')
    else:
        print('登录失败，请重新登录！ 提示：密码连续错误三次将被锁定！')

    #记录输入密码错误次数
    file  = open("peter_lock.txt",'w')
    num_3 = unm_2 + 1
#    print(num_3)
    file.write(str(num_3))
    file.close()

