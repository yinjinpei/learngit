# coding:utf-8
# author:YJ沛
#这里假设在登录某网站，需要验证用户和密码是否正确.

# 测试前先建立用户密码表，并插入数据：
'''
mysql> create table users(
    -> id int auto_increment primary key not null,
    -> name varchar(20),
    -> passwd char(40));

mysql> insert into users(name,passwd) values('peter','40bd001563085fc35165329ea1ff5c5ecbdbbeef')
mysql> insert into users(name,passwd) values('abc','40bd001563085fc35165329ea1ff5c5ecbdbbeef')

abc,peter用户的密码都为123
'''


# 之前封装好的mysql
from mysqlHelper import MysqlHelper
# 导入加密库
from hashlib import sha1


# 获得用户和密码
userName = input("请输入登录用户名：")
userPassed = input("请输入登录密码：")



# 密码加密
s1=sha1()
s1.update(userPassed.encode('utf-8'))
pwd=s1.hexdigest()
# print(type(pwd))
# print(pwd)

# 验证用户和密码
sql='select name,passwd from users where name=%s'
mysql=MysqlHelper('192.168.0.100',3306,'python3','jinpei','123456')
result=mysql.myselect(sql,[userName])
# print(type(result))
# print(result)
print(result)
# 匹配用户和用户的密码
if len(result)==0:
    print('用户名不存在!')
elif result[0][1] == pwd:
    print('登录成功！')
else:
    print('密码错误！')


