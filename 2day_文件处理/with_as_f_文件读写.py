#_*_ coding:utf-8 _*_

'''
with open('C:\PycharmProjects\learngit\\2day_文件处理\作业_购买商品\\test.txt','r') as file:
    for msg in file.readlines():
        print(msg.strip())
'''

def AlexReadines():
    with open('C:\PycharmProjects\learngit\\2day_文件处理\作业_购买商品\\test.txt','r') as file:
        seek = 0
        while True:
            file.seek(seek)
            data = file.readline()
            if data:
                seek = file.tell()
                yield data
            else:
                return


for i in AlexReadines():
    print(i.strip())
