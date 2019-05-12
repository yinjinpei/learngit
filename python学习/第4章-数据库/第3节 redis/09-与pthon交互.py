# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

到中文官网查找客户端代码
联网安装
sudo pip install redis

使用源码安装
unzip redis-py-master.zip
cd redis-py-master
sudo python setup.py install

交互代码

    引入模块
    import redis

    连接
    try:
        r=redis.StrictRedis(host='localhost',port=6379)
    except Exception,e:
        print e.message

方式一：根据数据类型的不同，调用相应的方法，完成读写
    更多方法同前面学的命令
    r.set('name','hello')
    r.get('name')

方式二：pipline
    缓冲多条命令，然后一次性执行，减少服务器-客户端之间TCP数据库包，从而提高效率
    pipe = r.pipeline()
    pipe.set('name', 'world')
    pipe.get('name')
    pipe.execute()

封装
    连接redis服务器部分是一致的
    这里将string类型的读写进行封装
    import redis
    class RedisHelper():
        def __init__(self,host='localhost',port=6379):
            self.__redis = redis.StrictRedis(host, port)
        def get(self,key):
            if self.__redis.exists(key):
                return self.__redis.get(key)
            else:
                return ""
        def set(self,key,value):
            self.__redis.set(key,value)
'''


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

re=RedisHelper('192.168.0.200',6379)

re.set('py2',222)
re.set('py3',333)

print(re.keys('*'))
print(re.get('py2'))

key_list=['py2','py3']
print(re.mget(key_list))




