# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

查找键，参数支持正则
KEYS pattern

判断键是否存在，如果存在返回1，不存在返回0
EXISTS key [key ...]

查看键对应的value的类型
TYPE key

删除键及对应的值
DEL key [key ...]

设置过期时间，以秒为单位
创建时没有设置过期时间则一直存在，直到使用使用DEL移除
EXPIRE key seconds

查看有效时间，以秒为单位
TTL key

'''

