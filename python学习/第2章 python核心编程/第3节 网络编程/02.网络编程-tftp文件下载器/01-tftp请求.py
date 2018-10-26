#-*- coding:utf-8 -*-
#author:YJ沛

from socket import *
import struct

# 1，获取要下载的文件名
downloadFileName = input("请输入要下载的文件名：")

# 2，创建套接字
udpsocket = socket(AF_INET,SOCK_DGRAM)

requestFileData = struct.pack("!H%dsb5sb"%len(downloadFileName), 1, downloadFileName.encode('utf-8'), 0, "octet".encode('utf-8') ,0)

udpsocket.sendto(requestFileData, ("172 122", 69))