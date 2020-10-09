# coding:utf-8
# author:YJ沛



import requests

response= requests.get("https://www.jianshu.com/p/ecb4d54ad8cf/")
response2= requests.get("https://www.cnblogs.com/jun-1024/p/10547374.html")
response.encoding='utf-8'
print(response.text)
print('response.status_code: ',response.status_code)
print('requests.codes.ok: ',requests.codes.ok)

if response.status_code == requests.codes.ok:
    print("访问成功")

# 可以直接使用状态码，更方便
if response.status_code == 200:
    print("访问成功")


import requests
# 发送请求
res = requests.get('https://www.baidu.com/')
# encoding设置编码
res.encoding ='utf-8'
# text 接收返回内容
print(res.text)