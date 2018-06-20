#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''
  编译登录接口
    1.输入用户名和密码
    2.认证成功后显示欢迎信息
    3.输错三次后锁定
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
else:
    file     = open("peter_lock.txt",'r')
    lock_num = file.readlines()

    file.close()

    unm_2 = int(lock_num)
    if unm_2 > 2:
        print('密码错误，因输入多次错误，帐号已被锁定，请联系管理员！')

    print('登录失败，请重新登录！ 提示：密码连续错误三次将被锁定！')
    file = open("peter_lock.txt",'w')
    infos = file.readlines()
    file.seek(0,0)
    for str in infos:
        if "0" in str:
            str = str.replace("0","1")
        elif "1" in str:
            str = str.replace("1", "2")
        elif "2" in str:
            str = str.replace("1", "3")
        else:
            print('haha')

    file.close()