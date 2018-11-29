#-*- coding:utf-8 -*-
#author:YJ沛


import pymysql

try:
    # conn = pymysql.connect(host='172.19.11.64', port=3306, user='jinpei', password="123456", database='python3', charset='utf8')
    conn = pymysql.Connect(
        host='172.19.11.64',
        port=3306,
        user='jinpei',
        passwd='123456',
        db='python3',
        charset='utf8'
    )

    cursorl = conn.cursor()

    sql = "INSERT INTO students (id, name, age) VALUES ( '%d', '%s', '%d' )"
    data = (3, "peter2", 11)
    cursorl.execute(sql % data)
    conn.commit()
    cursorl.close()
    conn.close()
except Exception as e:
    print(e)