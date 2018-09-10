#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
import datetime
import time
import re
from threading import Timer
from wxpy import  *

bot = Bot(cache_path=True)  # 生成登录二维码，开启缓存功能，短时间内不用扫描登录

allFriends = bot.friends(update=True)   # 获取所有微信好友
friends = []    # 储存指定微信好友，用于发送信息
nicknameList = []   # 储存指定微信好友的昵称

groups = [] #储存指定微信群，用于发送信息
groupNameList = []  #储存指定微信群的昵称
allGroups = bot.groups(update=True,contact_only=False)  # 获取微信所有群
allGroupName = []  # 储存所有群的昵称
for group in allGroups: #获取所有群的昵称
    allGroupName.append(group.name)
print(allGroupName) # for test

dateTime = None

def print_info():
    print('''
        微信助手 V1.0.0
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

    :param groupNameList:群名称
    '''
    for groupName in groupNameList:
        try:
            if bot.groups().search(nick_name=groupName)[0] in allGroups:
                groups.append(bot.groups().search(nick_name=groupName)[0])
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 请检查下填写的昵称是否正确！"%groupName)
            print("%s 请检查下填写的昵称是否正确！"%groupName)

def sendNews(groups_or_friends,msg,repeatSend=False,sendMsgCount=1):
    '''
    发送信息功能
    :param groups_or_friends:接收人或群
    :param msg: 发送内容
    :param repeatSend: 重复发送开关，默认为关闭
    :param sendMsgCount: 重复发送次数，与repeatSend一起使用
    '''

    # 控制重复发送次数，发送次数等于senMsgCount的值
    if sendMsgCount >= 1:
        sendMsgCount -= 1
    else:
        return

    # 发送信息给好友或群聊
    for obj in groups_or_friends:
        print(obj)  # for test
        obj.send(msg)

    # 给文件助手发信息
    # bot.file_helper.send(msg)

    # 否启动重复发送功能
    if repeatSend:
        t = Timer(5,sendNews,(groups_or_friends,msg,repeatSend,sendMsgCount))
        t.start()

def setTime(year,month,day,hour,minute,second):
    '''
    定时功能，以下为设置发送日期及时间
    :param year: 年
    :param month: 月
    :param day: 日
    :param hour: 时
    :param minute: 分
    :param second: 秒
    '''

    # 如设置在当前时间之前，将即时发送（年,  月,   日,  时,   分,    秒）
    startTime = datetime.datetime(year,month,day,hour,minute,second)
    while True:
        if startTime < datetime.datetime.now():
            break
        else:
            time.sleep(1)
            # print("时间没到,当前时间：%s" % datetime.datetime.now()) # for test

# 注册消息处理方法,charts为处理对象，except_self：是否不排除自己
@bot.register(chats=allFriends+allGroups,except_self=False)
def replyGroupsMsg(msg):
    '''
    自动回复好友和群聊功能
    :param msg: 定义自动回复的内容

    '''
    print(msg.sender.name, ':', msg.text, 'Msg Type:', msg.type)
    # msg.sender.mark_as_read()   # 消除当前聊天对象的未读提示小红点
    global allGroupName
    if msg.sender.name in allGroupName:   # 判断是群聊还是个人聊天
        if msg.is_at:  # 打印出所有群聊中@自己的文本消息，并自动回复相同内容
            print(msg)
            msg.reply("--------自动回复群聊中@到自己的信息----- for test ----")
        elif msg.text[:4] == '@所有人' or msg.text[:4].upper() == '@ALL':
            print(msg.text[:4])
            msg.reply("--------自动回复群聊中@到自己的信息----- for test ----")
        else:
            print(msg)
            print('没有被@到！！！！')
    else:
        #给好友自动回复信息
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

    num = input("请输入你要使用的功能：")
    while True:
        if num in '1234567':
            break
        else:
            num = input("输入有误，请重新输入：")

    # 给指定好友发消息
    if num == '1':
        # 添加好友昵称
        while True:
            friend_nickname = input("添加好友，请输入接收信息好友昵称：（输入exit结束添加）：")
            if friend_nickname == 'exit':
                break
            else:
                global nicknameList
                nicknameList.append(friend_nickname)
        print(nicknameList)
        # 添加好友昵称
        # global nicknameList
        # nicknameList = ['fangyueyan啦啦啦', 'TonyMr', '向春晓', '向春晓dfsdfsaf']

        sendFriendMsg = input("请输入需要发送的信息：")

        # 定时，传参顺序：年, 月, 日, 时, 分, 秒
        setTime(2018, 8, 30, 17, 14, 0)
        global dateTime
        dateTime = datetime.datetime.now()

        myFriends(nicknameList)
        sendNews(friends, sendFriendMsg)

    # 给所有好友发消息
    elif num == '2':
        sendFriendMsg = input("请输入需要发送的信息：")
        sendNews(allFriends,sendFriendMsg)

    # 给指定群发消息
    elif num == '3':
        # 添加群名
        while True:
            groupName = input("添加群，请输入接收信息群名（输入exit结束添加）： ")
            if groupName == 'exit':
                break
            else:
                global groupNameList
                groupNameList.append(groupName)
        print(groupNameList)    # for test
        sendGroupMsg = input("请输入需要发送的信息：")

        # global groupNameList
        # groupNameList = ['兄弟','XXX群组']

        myGroup(groupNameList)
        sendNews(groups,sendGroupMsg)
        # sendNews(groups,sendGroupMsg,True,3)

    # 给所有群发消息
    elif num == '4':
        pass

    elif num  == '7':
        embed() # 进入交互式的 Python 命令行界面，并堵塞当前线程


if __name__ == "__main__":
    main()

