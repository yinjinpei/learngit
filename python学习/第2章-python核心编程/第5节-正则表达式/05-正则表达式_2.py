# coding:utf-8
# author:YJ沛



import re


qq_mail = "455758880@qq.com"

result = re.match(r"[1-9]\d{5,11}@qq.com", qq_mail).group()
print(result)

