# def test(num):
#     print("-"*30)
#     def test2():
#         print("test2")
#     test2()
#     print(num)
#
# test(20)
#
#
# a = "my name is peter"
# b = [1,3,4,6,7,8]
# c = {"name":"peter","age":18}
# d = (11,33,66)
#
# print("""
# 字串符：%r，
# 列表：%r，
# 字典：%r，
# 元组：%r """%(a,b,c,d))
#

import time,datetime

#设置发送时间（年, 月, 日, 时, 分, 秒）
startTime = datetime.datetime(2018, 8, 30, 15, 23, 0)

while True:
    if startTime < datetime.datetime.now():
        print("现在时间是:")
        print(datetime.datetime.now())
        break
    else:
        time.sleep(1)
        print("时间还没到！ %s"%datetime.datetime.now())
