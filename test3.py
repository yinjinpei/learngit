import itchat, time, re
from itchat.content import *
#from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime


# 如果对方发的是文字，则我们给对方回复以下的东西
@itchat.msg_register([TEXT])
def text_reply(msg):
    itchat.send(('---  来自文字的回复 -----'), msg['FromUserName'])


# 如果对方发送的是图片，音频，视频和分享的东西我们都做出以下回复。
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    itchat.send(('---  来自图片，音频，视频和分享的回复 -----'), msg['FromUserName'])


itchat.auto_login(hotReload=True)
itchat.run()


# @itchat.msg_register([TEXT])
# def text_reply(msg):
#     match = re.search('年',msg['Text'])
#     if match:
#         itchat.send(('那我就祝你狗年大吉大利，新的一年事事顺心'),msg['FromUserName'])

# bot = Bot(cache_path=True)
#
# tu_ling = Tuling(api_key="自行注册")
#
# # chats指定对哪些用户起作用， 如果chats=None(默认值）对所有用户起作用
# @bot.register()
# def reply_msg(msg):
#     """
#     自动回复消息
#     :param msg: 接收到的信息数据
#     :return: 回复文本
#     """
#     # do_reply会自动回复消息并返回消息文本
#     tu_ling.do_reply(msg)