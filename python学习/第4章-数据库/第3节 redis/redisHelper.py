# coding:utf-8
# author:YJ沛


from redis import *


class RedisHelper():
    def __init__(self,hostname,port):
        self.__redis=StrictRedis(host=hostname,port=port)
    def set(self,key,value):
        self.__redis.set(key,value)
    def keys(self,key):
        return self.__redis.keys(key)
    def get(self,key):
        return self.__redis.get(key)
    def mget(self,key_list):
        # print(key_list)
        keys=[]
        for i in key_list:
            keys.append(self.__redis.mget(i))
        return keys

# re=RedisHelper('192.168.0.200',6379)
#
# re.set('py2',222)
# re.set('py3',333)
#
# print(re.keys('*'))
# print(re.get('py2'))
#
# key_list=['py2','py3']
# print(re.mget(key_list))




