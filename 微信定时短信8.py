#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
import datetime
import time
import re
from threading import Timer
from wxpy import  *

bot = Bot(cache_path=True)  # 生成登录二维码，做了缓存，短时间内不用扫描登录

allFriends = bot.friends(update=True)   # 获取所有好友的昵称
friends = []
nicknameList = []

allGroups = bot.groups(update=True,contact_only=False)  # 获取所有群聊名称
group_name = []  # 储存所有群的名称（字符串）
for group in allGroups:
    group_name.append(group.name)
print(group_name)

groups = []
groupNameList = []
# all_friend_group = []

dateTime = None


def print_info():
    print('''
    功能介绍：    
    1，给指定好友发消息
    2，给所有好友发消息
    3，给指定群发消息
    4，给所有群发消息
    5，定时发送消息
    6，重复发送（骚扰功能）
    7，自动回复

    ''')

def myFriends(nicknameList):
    '''获取要发送信息的好友昵称，添加到friends列表中'''

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

# # 获取所有类型的消息（好友消息、群聊、公众号，不包括任何自己发送的消息）
# # 并将获得的消息打印到控制台
# @bot.register()
# def print_others(msg):
#      print(msg)

@bot.register(chats=allFriends+allGroups,except_self=False)  # 注册消息处理方法
def Del_GroupMsg(msg):
    print(msg.sender.name, ':', msg.text, 'Msg Type:', msg.type)
    # msg.sender.mark_as_read()   # 消除当前聊天对象的未读提示小红点
    global group_name
    if msg.sender.name in group_name:
        print(msg.sender.name)
        print('在的。。。。。。')
        if msg.is_at:  # 打印出所有群聊中@自己的文本消息，并自动回复相同内容
            print(msg)
            msg.reply("--------自动回复群聊中@到自己的信息----- for test ----")
        else:
            print(msg)
            print('没有被@到！！！！')
    else:
        print('不在。。。。。。')
        if msg.type == TEXT:  # 接收的信息是纯文字处理
            macth = re.search("好", msg.text)
            if macth:  # 匹配关键字处理
                msg.reply_msg("----自动回复功能---匹配关键字：'好'----for test ----")
            else:
                msg.reply_msg("----自动回复功能---纯文字----for test ----")
        else:
            msg.reply_msg("----自动回复功能---其它----for test ----")

# embed()





def main():
    print_info()

    num = 2
    if num == 1:
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
        embed()

if __name__ == "__main__":
    main()

