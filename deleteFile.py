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
    offsettime = datetime.timedelta(days=-day)  # 计算偏移量,前10天
    re_date = (today + offsettime)  # 获取想要的日期的时间,即前10天时间
    # print("当前日期:" + today.strftime('%Y-%m-%d')) # for test
    # print("前10天日期:" + re_date.strftime('%Y-%m-%d')) # for test
    timestamp = time.mktime(re_date.timetuple())    # 前10天时间转换为时间戳
    return timestamp

# 处理过期文件
def fileHandle(timestamp, rootDir):
    deleteFileList = []  # 用来储存已过期的文件名
    fileList = os.listdir(rootDir)  # 获取目录下的文件
    try:
        fileList.remove('deleteFile.log')  # 排除当前目录下的deleteFile.log日志文件
    except ValueError:
        pass
    for file in fileList:
        filepath = os.path.join(rootDir, file)  # 获取文件修改时间,时间戳
        fileTime = os.path.getmtime(filepath)
        # 格式化时间
        timeArray = time.localtime(fileTime)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        if fileTime <= timestamp:
            deleteFileList.append(file)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)
            print(str(filepath), "---修改时间:" + otherStyleTime, "---超过10天,删除文件")
        else:
            print(str(filepath), "---修改时间:" + otherStyleTime, "---在10天内,无需处理!")
    return deleteFileList

# 记录操作日志,并写到本地
def logFileHandle(deleteFileList, rootDir):
    filepath = os.path.join(rootDir, 'deleteFile.log')
    fileNameList = ''
    for file in deleteFileList:
        fileNameList += str(file) + "\n"
    with open(filepath, 'a') as f:
        f.write("删除时间:" + str(datetime.datetime.now()) + "  删除的文件及目录如下:\n")
        f.write(str(fileNameList) + "\n")


def main():
    rootDir = 'D:\\Svn-Backup1'  # 需要删除的文件和目录存放的路径
    outTime = 10    # 文件和目录过期时间，即*天前，单位：天

    if not os.path.exists(rootDir):
        print(rootDir, '路径不存在,请检查下路径！！！')
        output = sys.stdout
        for i in range(10, -1, -1):
            time.sleep(1)
            output.write("\r将退出程序:{0}".format(i))
            output.flush()
        exit()
    timestamp = getTimestamp(outTime)
    deleteFileList = fileHandle(timestamp, rootDir)
    logFileHandle(deleteFileList, rootDir)


if __name__ == '__main__':
    main()
