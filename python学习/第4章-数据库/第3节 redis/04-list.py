# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

list
    列表的元素类型为string
    按照插入顺序排序
    在列表的头部或者尾部添加元素

命令

设置
    在头部插入数据
    LPUSH key value [value ...]

    在尾部插入数据
    RPUSH key value [value ...]

    在一个元素的前|后插入新元素
    LINSERT key BEFORE|AFTER pivot value

替换
    设置指定索引的元素值
    索引是基于0的下标
    索引可以是负数，表示偏移量是从list尾部开始计数，如-1表示列表的最后一个元素

    按索引替换
    LSET key index value


获取
    移除并且返回 key 对应的 list 的第一个元素
    LPOP key

    移除并返回存于 key 的 list 的最后一个元素
    RPOP key

    返回存储在 key 的列表里指定范围内的元素
    start 和 end 偏移量都是基于0的下标

    偏移量也可以是负数，表示偏移量是从list尾部开始计数，如-1表示列表的最后一个元素
    LRANGE key start stop

    例：显示所有值
    LRANGE key 0 -1

其它
    裁剪列表，改为原集合的一个子集
    start 和 end 偏移量都是基于0的下标

    偏移量也可以是负数，表示偏移量是从list尾部开始计数，如-1表示列表的最后一个元素
    LTRIM key start stop

    返回存储在 key 里的list的长度
    LLEN key

    返回列表里索引对应的元素
    LINDEX key index



'''

