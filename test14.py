# coding:utf-8
# author:YJ沛


title=     ['发布检查单', '需求说明书', '需求评审', '安全评审', '代码评审', 'SIT测试报告', 'UAT测试报告', '安全测试报告', '回归测试报告', '代码安全扫描报告', '代码质量扫描报告', 'SQM脚本审核报告', 'DBA脚本评审']

BRON_title_list=['发布检查单', '需求说明书', '需求评审', '安全评审', '代码评审', 'SIT测试报告', 'UAT测试报告', '安全测试报告', '回归测试报告']


a_dict={}
for ti in title:
    a_dict[ti]='X'

print(a_dict)

import re
text = 'This string1 is an example for match string2'
text= text.replace(' ','')   #去空格
print(text)
str=r'string5|string3|an|mat'

result = re.findall(str,text)   #分别匹配两种模式
if result:
    print(result)
else:
    print('空空如也')

