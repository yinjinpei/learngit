# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

set
    无序集合
    元素为string类型
    元素具有唯一性，不重复
命令

    设置
    添加元素
    SADD key member [member ...]

    获取
    返回key集合所有的元素
    SMEMBERS key

    返回集合元素个数
    SCARD key

其它

    求多个集合的交集
    SINTER key [key ...]

    求某集合与其它集合的差集
    SDIFF key [key ...]

    求多个集合的合集
    SUNION key [key ...]

    判断元素是否在集合中
    SISMEMBER key member


'''

