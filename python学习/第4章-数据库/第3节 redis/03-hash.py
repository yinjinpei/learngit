# coding:utf-8
# author:YJ沛



'''
hash用于存储对象，对象的格式为键值对

设置
    设置单个属性
    HSET key field value

    设置多个属性
    HMSET key field value [field value ...]

获取
    获取一个属性的值
    HGET key field

    获取多个属性的值
    HMGET key field [field ...]

    获取所有属性和值
    HGETALL key

    获取所有的属性
    HKEYS key

    返回包含属性的个数
    HLEN key

    获取所有值
    HVALS key

其它
    判断属性是否存在
    HEXISTS key field

    删除属性及值
    HDEL key field [field ...]

    返回值的字符串长度
    HSTRLEN key field

'''

