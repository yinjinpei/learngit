#-*- coding:utf-8 -*-
#author:YJ沛
from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime
# 添加需要接收消息的人的昵称，注意是写的是微信昵称，非备注名，也不是微信号，可添加多个
nickname = ['微信昵称1', '微信昵称2', '微信昵称3']

# 设置发送的内容
news = " 输入要发送的内容。----for test---- "

# 设置发送时间
# 如设置在当前时间之前，将即时发送（年, 月, 日, 时, 分, 秒）
startTime = datetime.datetime(2018, 8, 30, 17, 14, 0)

flag =False     # 重复发送(骚扰功能)，True：开启，False：不开启
interval = 60   # 设定发送消息间隔60秒
bot = Bot(cache_path=True)     # 生成登录二维码
dateTime = None

def send_news():
    try:
        friends = []
        for i in nickname:
            friends.append(bot.friends().search(i)[0])
        #发送消息
        for friend in friends:
            friend.send(news)
        print("消息已发送，发送时间: %s" % dateTime)

        #重复发送(骚扰功能)，设定时间间隔60秒，此功能默认不开启
        if flag:
            t = Timer(interval,send_news)
            t.start()
    except:
        print("发送失败。。。")

def timing():
    while True:
        if startTime < datetime.datetime.now():
            break
        else:
            time.sleep(1)
            print("时间没到,当前时间：%s" % datetime.datetime.now())

def main():
    timing()
    global dateTime
    dateTime = datetime.datetime.now()
    send_news()

if __name__ == "__main__":
    main()