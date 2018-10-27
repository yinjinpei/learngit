
'''
程序将文件夹内的所有文件重新命名，比如：旧:aa.txt，新:京东出品-aa.txt
1，输入文件夹名字
2，输入新的文件名字，
3，命名处理
'''
import os
dirName = input("请输入文件夹名字：")
newName = input("请输入新的文件名字：")

dirList = os.listdir(dirName)
os.chdir(dirName)

for oldFileName in dirList:
    newFileName = newName+"-"+oldFileName
    os.rename(oldFileName,newFileName)
