#-*- coding:utf-8 -*-
#author:YJ沛


'''
单播 ---> 点对点

多播 ---> 一对多

广播 ---> 对所有

'''


import socket, sys

#广播地址和端口 ，也可以这样写：dest = (192.168.1.255, 7788)   但这样写就限网段是192.168.1.0
dest = ('<broadcast>', 7788)


# 创建udp接字
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 对这个需要发送广播数据的套接字进行修改设置，否则不发送广播数据
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#