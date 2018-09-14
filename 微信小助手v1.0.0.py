# -*- coding:utf-8 -*-
# author:YJ沛

'''
微信助手-功能介绍：

    1，给指定好友发消息（定时，重复发送）
    2，给所有好友发消息（定时，重复发送）
    3，给指定群发消息（定时，重复发送）
    4，给所有群发消息（定时，重复发送）
    5，自动回复（自动回复，关键字回复，群聊被'@'、'@all' 或 '@所有人'回复）


使用说明：

    1，使用程序前需要安装python3环境以及安装第三方库：wxpy
    2，执行程序时，会自动生成二维码图片，用手机扫描二维码登录微信（其实就是登录网页版的微信）
    3，微信群可能会找不到，原因是一些不活跃的群可能无法被获取到，可通过在群内发言、
       修改群名称，或把群"保存到通讯录"的方式来激活，建议用最后一种方法，100%有效解决。
    4，给指定人发送消息时，填写的是"昵称"!!
    5，程序只在部分输入地方做了限制和异常处理，请按提示正常输入，避免异常。（不想花太多时间修改bug，哈哈。。。）
    6，功能2和3，本人没有测试过，因没有多余的测试微信号，各位自测吧。
    7，重复发送功能慎用，默认频率为1秒，小心被别人拉黑了@_@!!
'''

from __future__ import unicode_literals
from threading import Timer
import datetime
import time
import re
from wxpy import *  #第三方库


bot = Bot(cache_path=True)  # 生成登录二维码，开启缓存功能，短时间内不用扫描登录

allFriends = bot.friends(update=True)  # 获取所有微信好友
friends = []  # 储存指定微信好友，用于发送信息
nicknameList = []  # 储存指定微信好友的昵称

groups = []  # 储存指定微信群，用于发送信息
groupNameList = []  # 储存指定微信群的昵称
allGroups = bot.groups(update=True, contact_only=False)  # 获取微信所有群
allGroupName = []  # 储存微信所有群的昵称
for group in allGroups:  # 获取所有群的昵称
    allGroupName.append(group.name)
print('所获取的微信群名：',allGroupName)  # 打印所有群昵称 for test

keywordReply = None
keywordValue = None
sendFriendNewMsg = None
sendGroupNewMsg = None
repeatSend = True
sendMsgCount = 1

dateTime = None


def print_info():
    print('''
        微信助手 v1.0.0

    功能介绍：
    1，给指定好友发消息（定时，重复发送）
    2，给所有好友发消息（定时，重复发送）
    3，给指定群发消息（定时，重复发送）
    4，给所有群发消息（定时，重复发送）
    5，自动回复（自动回复，关键字回复，群聊被'@'回复）

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
            bot.file_helper.send("%s 不在您的好友列表中，请检查下填写的昵称是否正确！" % i)
            print("%s 不在您的好友列表中，请检查下填写的昵称是否正确！" % i)


def myGroup(groupNameList):
    '''
    获取匹配上的群聊名称，添加到groups列表中
    一些不活跃的群可能无法被获取到，可通过在群内发言，或修改群名称的方式来激活
    group = bot.groups().search(nick_name=groupName)  # 精确匹配群名
    group = bot.groups().search('groupName')  # 模糊匹配

    :param groupNameList:群名称
    '''
    for groupName in groupNameList:
        try:
            if bot.groups().search(nick_name=groupName)[0] in allGroups:
                groups.append(bot.groups().search(nick_name=groupName)[0])
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 请检查下填写的昵称是否正确！" % groupName)
            print("%s 请检查下填写的昵称是否正确！" % groupName)


def sendNews(groups_or_friends, msg, repeatSend=False, sendMsgCount=1):
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

    # 发送信息给好友或群
    for obj in groups_or_friends:
        print(obj)  # for test
        obj.send(msg)

    # 给文件助手发信息
    # bot.file_helper.send(msg)

    # 否启动重复发送功能
    if repeatSend:
        t = Timer(1, sendNews, (groups_or_friends, msg, repeatSend, sendMsgCount))
        t.start()


def setTime(year=1997, month=8, day=8, hour=8, minute=8, second=8):
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
    startTime = datetime.datetime(year, month, day, hour, minute, second)
    while True:
        if startTime < datetime.datetime.now():
            break
        else:
            time.sleep(1)
            print("时间没到,当前时间：%s" % datetime.datetime.now())  # 打印当前时间 ----for test


def repeatSend_sendTime():
    repeatSendValue = input("是否启动重发功能?  Y/N : ")
    if repeatSendValue == "Y" or repeatSendValue == "y":
        global repeatSend
        repeatSend = True
        while True:
            try:
                global sendMsgCount
                sendMsgCount = int(input("请输入重发次数 : "))
                if sendMsgCount > 0:
                    break
                else:
                    continue
            except Exception:
                print("输入格式不对，输入必须为正整数数字，请重新输入！")

    value = input("是否需要定时发送？ Y/N  : ")
    # 定时发送消息
    if value == "Y" or value == "y":
        while True:
            try:
                year = int(input("请输入 年份："))
                month = int(input("请输入 月份："))
                day = int(input("请输入 日份："))
                hour = int(input("请输入 时钟："))
                minute = int(input("请输入 分钟："))
                second = int(input("请输入 秒钟："))
                if year > 0 and month > 0 and day > 0 and hour >= 0 and minute >= 0 and second >= 0:
                    break
                else:
                    continue
            except Exception:
                print("输入格式不对，输入必须为自然数，请重新输入！")
        # 定时，传参顺序：年, 月, 日, 时, 分, 秒
        setTime(year, month, day, hour, minute, second)
        global dateTime
        dateTime = datetime.datetime.now()


# 注册消息处理方法,charts为处理对象，except_self：是否不排除自己
@bot.register(chats=allFriends + allGroups, except_self=False)
def replyMsg(msg):
    '''
    自动回复好友和群聊功能
    :param msg: 接收的消息的对象
    '''
    print(msg.sender.name, ':', msg.text, 'Msg Type:', msg.type)
    # msg.sender.mark_as_read()   # 消除当前聊天对象的未读提示小红点。为方便阅读，不做消除

    global allGroupName
    if msg.sender.name in allGroupName:  # 判断是群聊还是个人聊天
        if msg.is_at:  # 打印出所有群聊中@自己的文本消息，并自动回复相同内容
            print(msg)
            msg.reply(sendGroupNewMsg)
        elif msg.text[:4] == '@所有人' or msg.text[:4].upper() == '@ALL':
            print(msg.text[:4])
            msg.reply(sendGroupNewMsg)
        else:
            print(msg)
            print('没有被@到！！！！')  # for test
    else:
        # 给好友自动回复信息
        if msg.type == TEXT:  # 接收的信息是纯文字处理
            macth = re.search(str(keywordValue), msg.text)
            if macth:  # 匹配关键字处理
                msg.reply_msg(keywordReply)
            else:
                msg.reply_msg(sendFriendNewMsg)
        else:
            msg.reply_msg(sendFriendNewMsg)


def main():
    print_info()

    num = input("请输入你要使用的功能：")
    while True:
        if num in '12345':
            break
        else:
            num = input("输入有误，请重新输入：")

    # 给指定好友发消息
    if num == '1':
        # 添加好友昵称
        while True:
            friend_nickname = input("添加好友，请输入接收信息好友的昵称：（输入exit结束添加）：")
            if friend_nickname == 'exit':
                break
            else:
                global nicknameList
                nicknameList.append(friend_nickname)
        print(nicknameList)  # 打印所有添加的好友昵称 ----for test

        sendFriendMsg = input("请输入需要发送的信息：")
        repeatSend_sendTime()  # 定时发送和重复发送
        myFriends(nicknameList)
        sendNews(friends, sendFriendMsg, repeatSend, sendMsgCount)

    # 给所有好友发消息
    elif num == '2':
        sendFriendMsg = input("请输入需要发送的信息：")
        repeatSend_sendTime()  # 定时发送和重复发送
        sendNews(allFriends, sendFriendMsg, repeatSend, sendMsgCount)

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
        print(groupNameList)  # 打印所有添加的群 ----for test

        sendGroupMsg = input("请输入需要发送的信息：")
        repeatSend_sendTime()  # 定时发送和重复发送
        myGroup(groupNameList)
        sendNews(groups, sendGroupMsg, repeatSend, sendMsgCount)

    # 给所有群发消息
    elif num == '4':
        sendGroupMsg = input("请输入需要发送的信息：")
        repeatSend_sendTime()  # 定时发送和重复发送
        sendNews(allGroups, sendGroupMsg, repeatSend, sendMsgCount)

    # 自动回复功能
    elif num == '5':
        value = input("是否匹配关键字自动回复好友？  Y/N : ")
        if value == 'Y' or value == 'y':
            global keywordValue, keywordReply
            keywordValue = input("请输入关键字：")
            keywordReply = input("请输入回复带有关键字的信息内容：")

        global sendFriendNewMsg, sendGroupNewMsg
        sendFriendNewMsg = input("请输入需要回复好友的信息：")
        sendGroupNewMsg = input("请输入需要回复群中被@的信息：")

        embed()  # 进入交互式的 Python 命令行界面，并堵塞当前线程


if __name__ == "__main__":
    main()

