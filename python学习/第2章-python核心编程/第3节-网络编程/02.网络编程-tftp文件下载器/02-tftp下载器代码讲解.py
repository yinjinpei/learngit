#-*- coding:utf-8 -*-
#author:YJ沛



import struct
from socket import *
import time
import os


#0. 获取要下载的文件名字:
downloadFileName = input("请输入要下载的文件名:") # 20180914183818.gif

#1.创建socket
udpSocket = socket(AF_INET, SOCK_DGRAM)
requestFileData = struct.pack("!H%dsb5sb"%len(downloadFileName), 1, downloadFileName.encode('utf-8'), 0, "octet".encode("utf-8"), 0)

#2. 发送下载文件的请求
udpSocket.sendto(requestFileData, ("192.168.0.10", 69))

# flag = True #表示能够下载数据，即不擅长，如果是false那么就删除
# # num = 0
# # f = open(downloadFileName, "w")