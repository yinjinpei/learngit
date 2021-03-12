# -*- coding:utf-8 -*-
# 删除过期文件及目录

import os
import time
import datetime
import sys


# 处理\文件
def fileHandle(filePath):
    _deleteFileList = ''  # 用来储存将要删除的.zip文件
    fileList = os.listdir(filePath)  # 获取目录下所有文件
    _str = '.zip'
    _str2 = '.xlsx'

    for filename in fileList:
        if _str in filename or _str2 in filename:
            if os.path.isfile(filePath+'/'+filename):    # 如果是文件,则直接删除
                os.remove(filePath+'/'+filename)
                _deleteFileList += str(filename) + "\n"
            else:
                print('这不是一个zip或xlsx文件包：',filePath+'/'+filename)

    print("以下文件或目录修改时间已超过10天,将删除处理:\n" + _deleteFileList)
    return _deleteFileList

# 记录操作日志,并写到本地
def logFileHandle(deleteFileList, logPath):
    logfile = os.path.join(logPath, 'deleteFile.log')
    with open(logfile, 'a') as f:
        f.write("执行时间:" +
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
                "  删除的文件及目录如下:\n")
        f.write(str(deleteFileList) + "\n")

# 倒计器
def countdown(number):
    output = sys.stdout
    for i in range(number, -1, -1):
        output.write("\r将退出程序:{0}".format(i))
        output.flush()
        time.sleep(1)


def main():
    filePath = 'C:\\Users\\Administrator\\PycharmProjects\\learngit\\python学习\\第6章-Django\\startSoftware\\uploads\\temp'  # 需要删除的文件和目录存放的路径
    logPath =  'C:\\Users\\Administrator\\PycharmProjects\\learngit\\python学习\\第6章-Django\\startSoftware\\log'

    if not os.path.exists(filePath):
        print(filePath, '路径不存在,请检查下路径！！！')
        countdown(9)
        exit()

    deleteFileList = fileHandle(filePath)
    logFileHandle(deleteFileList, logPath)
    countdown(9)


if __name__ == '__main__':
    main()
