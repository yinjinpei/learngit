#-*- coding:utf-8 -*-
#author:YJ沛


from wxpy import *
#import TuLing
import re

bot = Bot(cache_path=True)
myFriend = bot.friends()  # 被处理消息的对象或对象集合

#myFriend += bot.groups().search('兄弟') #添加群
myFriend += bot.groups() #添加群


@bot.register(myFriend)  # 注册消息处理方法
def Del_GroupMsg(msg):
    print(msg.sender.name, ':', msg.text, 'Msg Type:', msg.type)
    #msg.sender.mark_as_read()   # 消除当前聊天对象的未读提示小红点

    if msg.is_at:   # 打印出所有群聊中@自己的文本消息，并自动回复相同内容
        print(msg)
        msg.reply("--------自动回复群聊中@到自己的信息---- for test ----")
    elif msg.type == TEXT:  # 接收的信息是纯文字处理
        macth = re.search("好", msg.text)
        if macth: # 匹配关键字处理
            msg.reply_msg("----自动回复功能---匹配关键字：'好'----for test ----")
        else:
            msg.reply_msg("----自动回复功能---纯文字----for test ----")
    else:
        msg.reply_msg("----自动回复功能---其它----for test ----")

embed()