#_*_ coding:utf-8 _*_

findMsg = input('请输入要查找的信息:')
count   = 0

file = open('NameFile.txt','r')
for i in file.readlines():
    Msg = i.find(findMsg)
    if Msg != -1:
        print(i.strip())
        count +=1
print('匹配到: %s 个 ' % count)
file.close()