# -*- coding:utf-8 -*-
# author:YJ沛

from __future__ import unicode_literals
from threading import Timer
import datetime
import time
import re
import xlrd
from wxpy import *


bot = Bot(cache_path=True)  # 生成登录二维码，开启缓存功能，短时间内不用扫描登录

allFriends = bot.friends(update=True)   # 获取所有微信好友
friends = []    # 储存指定微信好友，用于发送信息
nicknameList = []   # 储存指定微信好友的昵称

groups = []  # 储存指定微信群，用于发送信息
groupNameList = []  # 储存指定微信群的昵称
allGroups = bot.groups(update=True, contact_only=False)  # 获取微信所有群
allGroupName = []  # 储存微信所有群的昵称
for group in allGroups:  # 获取所有群的昵称
    allGroupName.append(group.name)
print(allGroupName)  # 打印所有群昵称 for test

keywordReply = None
keywordValue = None
sendFriendNewMsg = None
sendGroupNewMsg = None

dateTime = None
repeatSend = True
sendMsgCount = 1



# 注册消息处理方法,charts为处理对象，except_self：是否不排除自己
# @bot.register(chats=allFriends + allGroups, except_self=False)
@bot.register(except_self=False)
def replyMsg(msg):
    '''
    自动回复好友和群聊功能
    :param msg: 接收的消息类
    '''
    print(msg.sender.name, ':', msg.text, 'Msg Type:', msg.type)
    # msg.sender.mark_as_read()   # 消除当前聊天对象的未读提示小红点。为方便阅读，不做消除

    global allGroupName
    if msg.sender.name in allGroupName:   # 判断是群聊还是个人聊天
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

            # 匹配关键字处理
            if re.search(str(keywordValue[0]), msg.text):  # 判断是否为空，非空则执行
                find_name = msg.text[0:msg.text.rfind('手机', 1)]  # 获取联系人名字
                print('要查找的姓名',find_name)

                data = xlrd.open_workbook('personal_information.xls')
                sheet = data.sheet_by_name('Sheet1')  # 通过名称获取
                # print("工作表名称:", sheet.name)
                # print("行数:", sheet.nrows)
                # print("列数:", sheet.ncols)
                for i in range(0, sheet.nrows):
                    # print(sheet.row_values(i))
                    if find_name == sheet.row_values(i)[0]:
                        print("%s: %d "%(sheet.row_values(i)[0],sheet.row_values(i)[1]))
                        msg.reply_msg("%s: %d "%(sheet.row_values(i)[0],sheet.row_values(i)[1]))

            elif re.search(str(keywordValue[1]), msg.text):
                print('11111111111111')
                data = xlrd.open_workbook('personal_information.xls')
                print('11112222222222222')
                sheet = data.sheet_by_name('Sheet2')  # 通过名称获取
                print('33333333333333333333')
                print("工作表名称:", sheet.name)
                print("行数:", sheet.nrows)
                print("列数:", sheet.ncols)
                for i in range(0, sheet.nrows):
                    print("%s: %s " % (sheet.row_values(i)[0], sheet.row_values(i)[1]))
                    msg.reply_msg("%s: %s " % (sheet.row_values(i)[0], sheet.row_values(i)[1]))
            else:
                # msg.reply_msg(sendFriendNewMsg)
                pass


def main():

    # 自动回复功能

    global keywordValue, keywordReply
    keywordValue = ["手机","网址"]
    keywordReply = "好的"

    embed()  # 进入交互式的 Python 命令行界面，并堵塞当前线程



if __name__ == "__main__":
    main()
