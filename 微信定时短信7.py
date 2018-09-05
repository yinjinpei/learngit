#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime
import itchat, time, re


bot = None
allFriends = []
friends = []
nicknameList = []

allGroups = []
groups = []
groupNameList = []

dateTime = None


def myFriends(nicknameList):
    '''获取要发送信息的好友昵称，添加到friends列表中'''

    global allFriends
    allFriends = bot.friends(update=True)  # 获取所有好友的昵称

    # 添加需要接收消息的人的昵称，注意是写的是微信昵称，非备注名，也不是微信号，可添加多个
    for i in nicknameList:
        try:
            if bot.friends().search(i)[0] in allFriends:
                friends.append(bot.friends().search(i)[0])
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 不在您的好友列表中，请检查下填写的昵称是否正确！"%i)
            print("%s 不在您的好友列表中，请检查下填写的昵称是否正确！"%i)


def myGroup(groupNameList):
    '''
    获取匹配上的群聊名称，添加到groups列表中
    一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活

    group = bot.groups().search(nick_name=groupName)  # 精确匹配群名
    group = bot.groups().search('人')  # 模糊匹配
    '''

    bot.groups(update=True, contact_only=False)     #更新
    global allGroups
    allGroups = bot.groups()  # 获取所有群聊名

    for groupName in groupNameList:
        try:
            if bot.groups().search(nick_name=groupName)[0] in allGroups:
                groups.append(bot.groups().search(nick_name=groupName)[0])
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 请检查下填写的昵称是否正确！"%groupName)
            print("%s 请检查下填写的昵称是否正确！"%groupName)


def sendNews(groups_or_friends,msg,flag):
    for obj in groups_or_friends:
        print(obj)
        obj.send(msg)

    # bot.file_helper.send(msg)
    if flag == "True":
        t = Timer(5,sendNews,(groups_or_friends,msg,flag))
        t.start()


def set_time(year,month,day,hour,minute,second):
    # 设置发送时间
    # 如设置在当前时间之前，将即时发送（年,  月,   日,  时,   分,    秒）
    startTime = datetime.datetime(year,month,day,hour,minute,second)
    while True:
        if startTime < datetime.datetime.now():
            break
        else:
            time.sleep(1)
            print("时间没到,当前时间：%s" % datetime.datetime.now())


# 如果对方发的是文字，则我们给对方回复以下的东西
@itchat.msg_register([TEXT])
def text_reply(msg):
    itchat.send(('---  来自文字的回复 -----'), msg['FromUserName'])


# 如果对方发送的是图片，音频，视频和分享的东西我们都做出以下回复。
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    itchat.send(('---  来自图片，音频，视频和分享的回复 -----'), msg['FromUserName'])





def main():
    num = 2
    if num == 1:
        # 生成登录二维码，做了缓存，短时间内不用扫描登录
        global bot
        bot = Bot(cache_path=True)

        #定时，传参顺序：年, 月, 日, 时, 分, 秒
        set_time(2018, 8, 30, 17, 14, 0)
        global dateTime
        dateTime = datetime.datetime.now()

        # 添加好友昵称
        global nicknameList
        nicknameList = ['fangyueyan啦啦啦', 'TonyMr', '向春晓', '向春晓dfsdfsaf']

        global groupNameList
        groupNameList = ['兄弟','XXX群组']

        myFriends(nicknameList)
        myGroup(groupNameList)
        # print(friends)
        # print(groups)
        #
        # print(allFriends)
        # print(allGroups)

        # global msg
        # msg = "----- for test -----"
        # sendNews(groups,msg,"True")
    elif num  == 2:
        itchat.auto_login(hotReload=True)
        try:
            itchat.run()
        except Exception:
            print("有错。。。")


if __name__ == "__main__":
    main()

