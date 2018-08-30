#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime

# 生成登录二维码
bot = Bot()
dateTime = None

def send_news():
    try:
        #用来储存接收人的昵称
        friends = []
        #添加需要接收消息的人，注意是写的是微信昵称，非备注名，也不是微信号，可添加多个fangyueyan啦啦啦
        friends.append(bot.friends().search('TonyMr')[0])
        friends.append(bot.friends().search('向春晓')[0])

        # 设置发送的内容
        for friend in friends:
            friend.send('输入要发送的内容。----test-----')
        print("消息已发送，送发时间: %s" % dateTime)

        #重复发送，设定时间间隔60秒，此功能默认不开启
        #t = Timer(60,send_news)
        #t.start()
    except:
        print("定时发送失败。。。")

def set_time():
    # 设置发送时间
    # 如设置在当前时间之前，将即时发送（年, 月, 日, 时, 分, 秒）
    startTime = datetime.datetime(2018, 8, 30, 17, 14, 0)
    while True:
        if startTime < datetime.datetime.now():
            break
        else:
            time.sleep(1)
            print("时间没到,当前时间：%s" % datetime.datetime.now())

def main():
    set_time()
    global dateTime
    dateTime = datetime.datetime.now()
    send_news()

if __name__ == "__main__":
    main()