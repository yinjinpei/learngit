# coding:utf-8
# author:YJ沛


# 调用封装好的mysql-->mysqlHelper.py
from mysqlHelper import MysqlHelper

sql_user = input("请输入数据库用户名：")
sql_passwd = input("请输入数据库用户密码：")

# 更新数据
# sql="update students set name=%s where id=%s"
# params=['李青天',17]
# mysql=MysqlHelper('192.168.31.100',3306,'python3',sql_user,sql_passwd)
# mysql.cud(sql,params)

# 插入数据
# sql2="insert into students(name) values(%s)"
# params2=['胡歌']
# mysql2=MysqlHelper('192.168.31.100',3306,'python3',sql_user,sql_passwd)
# mysql2.cud(sql2,params2)

# 查询
sql3="select id,name from students where id<8"
mysql3=MysqlHelper('192.168.31.100',3306,'python3',sql_user,sql_passwd)
result=mysql3.myselect(sql3)
print(result)
