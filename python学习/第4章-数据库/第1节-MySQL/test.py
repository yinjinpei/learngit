# coding:utf-8
# author:YJ沛


import hashlib

md5 = hashlib.md5()
md5.update(b'how to use md5 in ')
md5.update(b'python hashlib?')
print(md5.hexdigest())


md5test2 = hashlib.md5()
str='how to use md5 in python hashlib?'
md5test2.update(str.encode('utf-8'))
print(md5test2.hexdigest())