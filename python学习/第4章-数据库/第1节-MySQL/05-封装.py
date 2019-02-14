# coding=utf-8
# author:YJ沛
# 和mysqlHelper.py一样的，修改了名字为了可以被调用

import pymysql


import pymysql


class MysqlHelper:
    def __init__(self, host, port, db, user, password, charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset

    def open(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def cud(self, sql, params):
        try:
            self.open()

            self.cursor.execute(sql, params)
            self.conn.commit()

            self.close()
            print("sql语句执行完成！")

        except Exception as e:
            print(e)

    def myselect(self,sql,params=[]):
        try:
            self.open()

            self.cursor.execute(sql,params)
            result = self.cursor.fetchall()

            self.close()
            print("sql语句执行完成！")
            return result

        except Exception as e:
            print(e)