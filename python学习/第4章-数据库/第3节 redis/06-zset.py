# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

zset
    sorted set，有序集合(序号从0开始，尾是-1)
    元素为string类型
    元素具有唯一性，不重复
    每个元素都会关联一个double类型的score，表示权重，通过权重将元素从小到大排序
    元素的score可以相同

命令
    设置
    添加
    ZADD key score member [score member ...]

获取
    返回指定范围内的元素
    ZRANGE key start stop


    返回元素个数
    ZCARD key

    返回有序集key中，score值在min和max之间的成员个数
    ZCOUNT key min max

    返回有序集key中，成员member的score值，即元素所在的序号（序号=序号+1）（索引）
    ZSCORE key member

'''

