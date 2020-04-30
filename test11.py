# coding:utf-8
# author:YJ沛

import re

text = 'uploads/peter/新建文件夹/constantly-15.1.0-py2.py3-none-any.whl'

patten = re.compile(r'.+?/')

result = patten.findall(text)
print(result)