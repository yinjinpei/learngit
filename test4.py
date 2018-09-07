import itchat, time, re
from itchat.content import *
#from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime


bot = Bot(cache_path=True)

# 给机器人自己发送消息
bot.self.send('Hello World!')
# 给文件传输助手发送消息
bot.file_helper.send('Hello World!')

# # 查找昵称为'乙醚。'的好友
# my_friend = bot.friends().search(u'乙醚。')[0]
# # <Friend: 乙醚。>


# 获取所有类型的消息（好友消息、群聊、公众号，不包括任何自己发送的消息）
# 并将获得的消息打印到控制台
@bot.register()
def print_others(msg):
    print(msg)

#
# # 回复 my_friend 发送的消息
# @bot.register(my_friend)
# def reply_my_friend(msg):
#     return 'received: {} ({})'.format(msg.text, msg.type)

# 回复发送给自己的消息，可以使用这个方法来进行测试机器人而不影响到他人
@bot.register(bot.self, msg_types=TEXT, except_self=False)
def reply_self(msg):
    print(msg)
    return 'received: {} ({})'.format(msg.text, msg.type)

# 打印出所有群聊中@自己的文本消息，并自动回复相同内容
# 这条注册消息是我们构建群聊机器人的基础
@bot.register(Group, TEXT)
def print_group_msg(msg):
    if msg.is_at:
        print(msg)
        msg.reply(msg.text)


# 进入 Python 命令行、让程序保持运行
# 推荐使用
embed()

# 或者仅仅堵塞线程
# bot.join()