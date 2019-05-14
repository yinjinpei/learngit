#-*- coding:utf-8 -*-
# author:YJ沛
# 用户登录


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

if userName == None or userPasswd == None:
    print("用户和密码不能为空")
    sys.exit()

# redis用户登录验证
r_redis=RedisHelper('192.168.43.64',6379)
if r_redis.get(userName) == pwd:
        print("登录成功")
else:
    r_mysql=MysqlHelper(host='192.168.43.64', port=3306, db='python3', user=userName, password=pwd, charset='utf8')




# mysql用户登录验证



