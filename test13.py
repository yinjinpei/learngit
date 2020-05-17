# coding:utf-8
# author:YJ沛


# !/usr/bin/python
import re,os

line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")

domain_name="BRON-COMS"
version="1.1.0"
produce_date="20200514"
produce_date2="2020-05-14"

# backend_report=[{"checklist":"发布检查单"},{"demand_doc":"需求说明书"},{"demand_review":"需求评审"},
#                 {"safety_review":"安全评审"},{"code_review":"代码评审"},{"sit_report":"SIT测试报告"},
#                 {"uat_report":"UAT测试报告"},{"safety_report":"安全测试报告"},
#                 {"code_security_scan_report":"代码安全扫描报告"},{"code_quality_scan_report":"代码质量扫描报告"},
#                 {"sqm_report":"SQM脚本审核报告"},{"dba_review":"DBA脚本评审"},{"regress_review":"回归测试报告"}]
# front_report=[{"checklist":"发布检查单"},{"demand_doc":"需求说明书"},{"demand_review":"需求评审"},
#               {"safety_review":"安全评审"},{"code_review":"代码评审"},{"sit_report":"SIT测试报告"},
#               {"uat_report":"UAT测试报告"},{"safety_report":"安全测试报告"},{"regress_review":"回归测试报告"}]

backend_report={"checklist":"发布检查单","demand_doc":"需求说明书","demand_review":"需求评审","safety_review":"安全评审",
                 "code_review":"代码评审","sit_report":"SIT测试报告","uat_report":"UAT测试报告","safety_report":"安全测试报告",
                 "code_security_scan_report":"代码安全扫描报告","code_quality_scan_report":"代码质量扫描报告",
                 "sqm_report":"SQM脚本审核报告","dba_review":"DBA脚本评审","regress_review":"回归测试报告"}

front_report={"checklist":"发布检查单","demand_doc":"需求说明书","demand_review":"需求评审","safety_review":"安全评审",
              "code_review":"代码评审","sit_report":"SIT测试报告","uat_report":"UAT测试报告",
              "safety_report":"安全测试报告","regress_review":"回归测试报告"}

user_path='C:\\Users\\Administrator\\PycharmProjects\\learngit\\python学习\\第6章-Django\\startSoftware\\uploads\\shar\\BCOS-MNGT\\BCOS-MNGT1.1.0（2020-05-10）'
file_list=os.listdir(user_path)

# file_name="BRON-COMS1.1.0_20200514版本_口袋升级2.0_需求说明书.doc"
file_name="BRON-COMS_1.1.0_20200514版本d22_3456口袋升级2.0_我也不知道呀需求说明书"

matchStr=re.match("%s(.*)%s(.*)%s(.*)%s(.*)"%(domain_name,version,produce_date,'需求说明书'), file_name, re.M | re.I )

a='√'
b='X'
print(a,b)

key_list=backend_report.keys()

for key in key_list:
    print(key,end='' )
    print(backend_report.get(key))

a={'a':'111'}
print(a['a'])

if a['a'] == '111':
    print('没错')
else:
    print('错了！！')

print(matchStr.group())



import re
xyz='BCOS-MNGT512'
m=re.search('\d{1,2}$', xyz)
print(m)
print(xyz[m.start():m.end()])


a = ['a1','a2']
b = ['b1','b2']
c = [a,b]
print(dict(c)) # {'a1': 'a2', 'b1': 'b2'}
# 相当于遍历子列表，如下
dit = {}
for i in c:
    dit[i[0]] = i[1]
print(dit)


a=[1,2]

c,d=a

print(c)
print(d)
