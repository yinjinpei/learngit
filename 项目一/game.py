# coding:utf-8
# author:YJ沛

import psutil


# def judgeprocess(processname):
#     pl = psutil.pids()
#     for pid in pl:
#         if psutil.Process(pid).name() == processname:
#             print(pid)
#             break
#     else:
#         print("not found")
#
#
# if judgeprocess('华龙殷少002') == 0:
#     print('success')
# else:
#     pass

p=psutil.Process(10772)
print(p.uids())