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
# #
#
# import time,datetime
#
# #设置发送时间（年, 月, 日, 时, 分, 秒）
# startTime = datetime.datetime(2018, 8, 30, 15, 23, 0)
#
# while True:
#     if startTime < datetime.datetime.now():
#         print("现在时间是:")
#         print(datetime.datetime.now())
#         break
#     else:
#         time.sleep(1)
#         print("时间还没到！ %s"%datetime.datetime.now())
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
#
# import time,datetime
#
# #设置发送时间（年, 月, 日, 时, 分, 秒）
# startTime = datetime.datetime(2018, 8, 30, 15, 23, 0)
#
# while True:
#     if startTime < datetime.datetime.now():
#         print("现在时间是:")
#         print(datetime.datetime.now())
#         break
#     else:
#         time.sleep(1)
#         print("时间还没到！ %s"%datetime.datetime.now())



from threading import Timer
from wxpy import  *
import time,datetime
import itchat

# itchat.auto_login(hotReload=True)
#
# # def send_msg(msg,gname):
# #     rooms = itchat.get_chatrooms(update=True)
# #     if rooms is not None:
# #         print(rooms)
# #     else:
# #         print("空的")
#
# rooms = itchat.get_chatrooms(update=True)
# #rooms = itchat.search_chatrooms(name="紫川")
# if rooms is not None:
#     print(len(rooms))
#     print(rooms)
#     for i in rooms:
#         #print(type(i))
#         #print(type(i['MemberList']))
#         for j in i['MemberList']:
#             print(j["NickName"])
#
# else:
#     print("空的")


'''
Created on 2013-7-31
@author: Eric
'''
import time
from threading import Timer


def timer_start():
    t = Timer(1, test_func, ("Parameter1",))
    t.start()


def test_func(msg1):
    print("I'm test_func,", msg1)
    timer_start()


def timer2():
    timer_start()
    # while True:
    #     time.sleep(1)


if __name__ == "__main__":
    timer2()