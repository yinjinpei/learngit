#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime

# 生成登录二维码
bot = Bot(cache_path=True)
#dateTime = None

#bot.file_helper.send('hello')   #给 文件传输助手 发消息

# def send_news():
#     try:
#         # 添加需要接收消息的人的昵称，注意是写的是微信昵称，非备注名，也不是微信号，可添加多个
#         nickname = ['微信昵称1','微信昵称2','微信昵称3']
#
#         friends = []
#         for i in nickname:
#             friends.append(bot.friends().search(i)[0])
#
#         # 设置发送的内容
#         for friend in friends:
#             friend.send('输入要发送的内容。----for test----')
#         print("消息已发送，发送时间: %s" % dateTime)
#
#         #重复发送(骚扰功能)，设定时间间隔60秒，此功能默认不开启
#         #t = Timer(60,send_news)
#         #t.start()
#     except:
#         print("发送失败。。。")
#
# def set_time():
#     # 设置发送时间
#     # 如设置在当前时间之前，将即时发送（年, 月, 日, 时, 分, 秒）
#     startTime = datetime.datetime(2018, 8, 30, 17, 14, 0)
#     while True:
#         if startTime < datetime.datetime.now():
#             break
#         else:
#             time.sleep(1)
#             print("时间没到,当前时间：%s" % datetime.datetime.now())
#
# def main():
#     set_time()
#     global dateTime
#     dateTime = datetime.datetime.now()
#     send_news()
#
# if __name__ == "__main__":
#     main()

bot.groups(update=True, contact_only=False)
group = bot.groups().search('漂车')[0]    #模糊匹配
print(group)
#group.send("@all 各位，这个星期四之前把要报销车票发到我微信上，我调休不在公司，所以不要发到我邮箱，谢谢！！！")

#friends = bot.friends()
#print(friends)
#for friend in friends:
#    print(friend)

group2 = bot.groups().search()