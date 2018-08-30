#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import requests

#生成登录二维码
bot=Bot()

def get_news():
    '''金山词霸英文和翻译'''
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content,note

def send_news():
    try:
        # contents = get_news()
        my_friend = bot.friends().search(u'香蜜湖BBQ')[0]
        # my_friend.send(contents[0])
        # my_friend.send(contents[1])
        my_friend.send(u'两个250!')
        t = Timer(60,send_news)
        t.start()

    except:
        my_friend = bot.friends().search(u'fangyueyan啦啦啦')[0]
        my_friend.send(u'发送失败。。')

if __name__ == "__main__":
    send_news()