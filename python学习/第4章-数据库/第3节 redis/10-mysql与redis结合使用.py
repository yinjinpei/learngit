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
# print(pwd)

if len(userName) == 0 or len(userPasswd) == 0:
    print("用户和密码不能为空")
    sys.exit()

# redis用户登录验证
# r_redis=RedisHelper('192.168.43.64',6379)
r_redis=RedisHelper('192.168.0.200',6379)
pwd1=r_redis.get(userName)

# 先到redis匹配
if pwd1:
    if pwd1.decode('utf8') == pwd:
        print("登录成功! 来自redis")
    else:
        print("密码错误！")
else:
    sql = "select passwd from users where name=%s"
    params=[userName]
    # r_mysql=MysqlHelper(host='192.168.43.64', port=3306, db='python3', user=userName, password=pwd, charset='utf8')
    r_mysql = MysqlHelper('192.168.0.100', 3306, 'python3', 'peter', '123456', 'utf8')
    result=r_mysql.myselect(sql,params)
    print(result)

    if len(result) == 0:
        print("用户不存在")
    else:
        if result[0][0] == pwd:
            # 如果用户和密码都正确的，则写入redis
            r_redis.set(userName,pwd)

            print("登录成功! 来自mysql")
        else:
            print("密码错误！")




# mysql用户登录验证



