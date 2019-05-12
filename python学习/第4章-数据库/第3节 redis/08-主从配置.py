# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

一个master可以拥有多个slave，一个slave又可以拥有多个slave，如此下去，形成了强大的多级服务器集群架构
比如，将ip为192.168.1.10的机器作为主服务器，将ip为192.168.1.11的机器作为从服务器

设置主服务器的配置
    bind 192.168.1.10

设置从服务器的配置
    注意：在slaveof后面写主机ip，再写端口，而且端口必须写
    bind 192.168.1.11
    slaveof 192.168.1.10 6379

在master和slave分别执行info命令，查看输出信息
    在master上写数据
    set hello world

    在slave上读数据
    get hello


'''

