#coding=utf-8
#author:YJ沛


'''
安装mysql模块
sudo apt-get install python-mysql
在文件中引入模块
import Mysqldb

Connection对象
用于建立与数据库的连接

创建对象：调用connect()方法
conn=connect(参数列表)
    参数host：连接的mysql主机，如果本机是'localhost'
    参数port：连接的mysql主机的端口，默认是3306
    参数db：数据库的名称
    参数user：连接的用户名
    参数password：连接的密码
    参数charset：通信采用的编码方式，默认是'gb2312'，要求与数据库创建时指定的编码一致，否则中文会乱码
    对象的方法

close()关闭连接
commit()事务，所以需要提交才会生效
rollback()事务，放弃之前的操作
cursor()返回Cursor对象，用于执行sql语句并获得结果

Cursor对象
执行sql语句
创建对象：调用Connection对象的cursor()方法
cursor1=conn.cursor()

对象的方法
close()关闭

execute(operation [, parameters ])执行语句，返回受影响的行数
fetchone()执行查询语句时，获取查询结果集的第一个行数据，返回一个元组
next()执行查询语句时，获取当前行的下一行
fetchall()执行查询时，获取结果集的所有行，一行构成一个元组，再将这些元组装入一个元组返回

scroll(value[,mode])将行指针移动到某个位置
    mode表示移动的方式
    mode的默认值为relative，表示基于当前行移动到value，value为正则向下移动，value为负则向上移动
    mode的值为absolute，表示基于第一条数据的位置，第一条数据的位置为0

对象的属性
rowcount只读属性，表示最近一次execute()执行后受影响的行数
connection获得当前连接对象

'''

import pymysql


user_name = input("请输入用户名：")
try:
    # conn = pymysql.connect(host='172.19.11.64', port=3306, user='jinpei', password="123456", database='python3', charset='utf8')
    conn = pymysql.Connect(
        host='192.168.31.100',
        port=3306,
        user='jinpei',
        passwd='123456',
        db='python3',
        charset='utf8'
    )

    cursor1 = conn.cursor()

    # 插入数据
    # sql = "INSERT INTO students (id, name, birthday) VALUES ( '%d', '%s', '%s' )"
    # data = (10, "peter2", '1993-11-1')
    # cursor1.execute(sql % data)

    # cursor1.execute("INSERT INTO students(id,name,birthday) VALUES(12,'郭靖','1982-8-8')")

    # 更新数据
    # cursor1.execute("update students set gender=0 where name = '茜茜'")

    #删除数据
    # cursor1.execute("delete from students where name='郭靖'")

    # 参数化传参  这样用户就可以输入任意字符了
    sql="insert into students(name) values(%s)"
    cursor1.execute(sql,[user_name])


    conn.commit()
    cursor1.close()
    conn.close()
except Exception as e:
    print(e)