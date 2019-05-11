# coding:utf-8
# author:YJ沛

'''
官网：https://www.mongodb.com/download-center/community
下载：https://www.mongodb.org/dl/linux

MongonDB是非关系型数据库

三元素：数据库、集合、文档
    集合就是关系数据库的表
    文档对应关系数据库中的行

    文档，就是一个对象，由键值对构成，是json的扩展Bson形式
    {'name':'guojing','gender':'男'}

    集合：类似于关系数据库中的表，储存多个文档，结构不固定，如可以存储如下文档在一个集合中
    {'name':'guojing','gender':'男'}
    {'name':'huangrong','age':18}
    {'book':'shuihuzhuan','heros':'108'}

    数据库：是一个集合的物理容器，一个数据库中可以包含多个文档
    一个服务器通常有多个数据库




'''