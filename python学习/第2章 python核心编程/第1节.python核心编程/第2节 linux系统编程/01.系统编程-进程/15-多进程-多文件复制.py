#-*- coding:utf-8 -*-
#author:YJ沛

from multiprocessing import Pool,Manager,Queue
import os


def write(name, odlFolderName, newFolderName, q):
    '''完成复制一个文件的功能'''
    fr = open(odlFolderName+"/"+name,'r',encoding='UTF-8')
    fw = open(newFolderName+"/"+name, "w",encoding='UTF-8')
    while True:
        str = fr.read(1024)
        if str:
            fw.write(str)
        else:
            # print(name,"这个文件完成") for test
            break


    fr.close()
    fw.close()
    q.put(name)

def main():
    # 1，读取原文件夹名
    odlFolderName = input("请输入你的原的文件夹名：")

    # 2，创建新的文件夹
    newFolderName = odlFolderName+'_备份'
    #print(newFolderName)    # for test
    os.mkdir(newFolderName)

    # 3，获取原文件中的所有文件名
    fileNames = os.listdir(odlFolderName)
    #print(fileNames)    # for test

    # 4，复制原文件夹中的所有文件(有多个文件则添加多少个进程)
    q = Manager().Queue()
    pool = Pool(2)
    for name in fileNames:
        pool.apply_async(write,args=(name,odlFolderName,newFolderName,q))

    pool.close()
    pool.join()

    num = 0
    allNum = len(fileNames)
    while True:
        try:
            q.get(True,0.1)
        except Exception:
            pass
        num +=1
        sum = num/allNum
        print('\r copy 的进度是：%.2f%%'%(sum*100),end='')
        if num == allNum:
            print('---------------------')
            print('复制完成了！！！！')
            break
        else:
            pass


if __name__ == '__main__':
    main()