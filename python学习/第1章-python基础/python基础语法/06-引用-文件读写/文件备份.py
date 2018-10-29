'''
备份一个文件名，如：test.py --> test[复件].py

'''

oldFileName = input("请输入你想要备份的文件名：")

f = open("filedir/"+oldFileName,"r")

seek = oldFileName.rfind(".")   #找出后缀位置
newFileName = oldFileName[0:seek]+"[复件]"+oldFileName[seek:] #取前缀名字并重新命名:xxx[复件].xx
f2 = open("filedir/"+newFileName,"w+")

while True:
    str = f.read(1024)  #每次只读1K文件大小，防止文件过大导致内存错误
    if len(str) == 0:    #当文件读完退出读写操作
        break
    f2.write(str)

f.close()
f2.close()