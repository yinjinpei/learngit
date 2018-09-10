
'''
程序将文件批量修改（去除前缀logo），如旧：新-沛哥出品-test.py  新：test.py
1，输入文件夹名字
2，输入去除前缀logo分割符，如"-"
3，命名处理
'''

import os

dirName = input("请输入文件夹名字：")
logo = input("输入去除前缀logo分割符：")
dirList = os.listdir(dirName)
os.chdir(dirName)

for oldFileName in dirList:
    sign = oldFileName.rfind(logo)
    newFileName = oldFileName[sign+1:]
    os.rename(oldFileName,newFileName)