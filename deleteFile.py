# -*- coding:utf-8 -*-
# 删除过期文件及目录

import os
import time
import datetime
import shutil
import sys


# 获取超时时间戳
def getTimestamp(day):
    today = datetime.datetime.now()  # 获取当前时间
    offsettime = datetime.timedelta(days=-day)  # 计算偏移量,前*天
    re_date = (today + offsettime)  # 获取想要的日期的时间,即前*天时间
    timestamp = time.mktime(re_date.timetuple())    # 前*天时间转换为时间戳
    return timestamp

# 处理过期文件
def fileHandle(timestamp, rootDir):
    _deleteFileList = ''  # 用来储存所有已过期的文件名或目录名
    _reservedFileList = ''   # 用来储存所有未过期的文件名或目录名
    fileList = os.listdir(rootDir)  # 获取目录下所有文件
    try:
        fileList.remove('deleteFile.log')  # 排除当前目录下的deleteFile.log日志文件
    except ValueError:
        pass

    for file in fileList:
        filepath = os.path.join(rootDir, file)
        fileTime = os.path.getmtime(filepath)   # 获取文件或目录修改时间,时间戳

        if fileTime <= timestamp:
            _deleteFileList += str(file) + "\n"
            if os.path.isfile(filepath):    # 如果是文件,则直接删除
                os.remove(filepath)
            elif os.path.isdir(filepath):   # 如果是目录,则删除目录及目录下所有文件
                shutil.rmtree(filepath, True)
        else:
            _reservedFileList += str(file) + "\n"
    print("以下文件或目录修改时间已超过10天,将删除处理:\n" + _deleteFileList)
    print("以下文件或目录修改时间在10天内,无需处理:\n" + _reservedFileList)
    return _deleteFileList

# 记录操作日志,并写到本地
def logFileHandle(deleteFileList, rootDir):
    filepath = os.path.join(rootDir, 'deleteFile.log')
    with open(filepath, 'a') as f:
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
    rootDir = 'D:\\Svn-Backup'  # 需要删除的文件和目录存放的路径
    outTime = 10    # 文件和目录过期时间，即*天前，单位：天

    if not os.path.exists(rootDir):
        print(rootDir, '路径不存在,请检查下路径！！！')
        countdown(9)
        exit()

    timestamp = getTimestamp(outTime)
    deleteFileList = fileHandle(timestamp, rootDir)
    logFileHandle(deleteFileList, rootDir)
    countdown(9)


if __name__ == '__main__':
    main()
