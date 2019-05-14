# coding:utf-8
# author:YJ沛


import sys
# 导入加密库
from hashlib import sha1
# 之前封装好的mysql
from mysqlHelper import MysqlHelper
# 之前封装好的redis
from redisHelper import RedisHelper


userName=input("请输入用户名：")
userPasswd=input("请输入密码：")

s1=sha1()
s1.update(userPasswd.encode('utf-8'))
pwd=s1.hexdigest()
print(pwd)


sql = "select passwd from users where name=%s"

# r_mysql=MysqlHelper(host='192.168.43.64', port=3306, db='python3', user=userName, password=pwd, charset='utf8')
r_mysql = MysqlHelper('192.168.0.100', 3306, 'python3', 'peter', '123456', 'utf8')
result = r_mysql.myselect(sql, [userName])
print(result)

if result==None:
    print('空的')
else:
    print('不空的')