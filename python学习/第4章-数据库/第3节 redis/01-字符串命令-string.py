# coding:utf-8
# author:YJ沛



'''
string
    最大能储512MB数据

设置
    设置键值
    set key value

    设置键值及过期时间，以秒为单位
    SETEX key seconds value

    设置多个键值
    MSET key value [key value ...]

获取
    根据键获取值，如果不存在此键则返回nil
    GET key

    根据多个键获取多个值
    MGET key [key ...]

运算
    要求：值是数字
    将key对应的value加1
    INCR key

    将key对应的value加整数
    INCRBY key increment

    将key对应的value减1
    DECR key

    将key对应的value减整数
    DECRBY key decrement

其它
    追加值
    APPEND key value

    获取值长度
    STRLEN key
'''

