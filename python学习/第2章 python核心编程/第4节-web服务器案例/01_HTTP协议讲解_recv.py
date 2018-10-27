#-*- coding:utf-8 -*-
#author:YJ沛


'''
HTTP请求方式：
    GET     获取数据
    POST    修改数据
    PUT     保存数据
    DELETE  删除
    OPTION  询问服务器的某支持特性
    HEAD    返回报文头

'''

'''
URI ：URL，URN

查询字符串Query String: ?xxxxxxxxxxxxx

'''


'''
python：两个空瓶可以换一瓶啤酒，四个瓶盖可以换一瓶啤酒，一开始你有十瓶啤酒，最后你能喝到几瓶？（
        这里我们假定你能一直喝下去）请+大神解决！！！很急
'''

class Beer():
    ''' status=0表示为空瓶，status=1则不是空的'''
    def __init__(self,number,status):
        self.beer_number = number
        self.beer_status = status


class People():
    def drink(self,number):
        Beer(number,0)
        return






