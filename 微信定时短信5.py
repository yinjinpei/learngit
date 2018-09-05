#-*- coding:utf-8 -*-
#author:YJ沛
'''
1，给好友发信息
	1，单发
	2，多发
	3，全发
2，群发
	1，单群发
	2，多群发
	3，全发
3，定时发信息
	1，好友发
	2，群发
4，骚扰功能
	1，单发
	2，多发
	3，全发

'''

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime


# 生成登录二维码，做了缓存，短时间内不用扫描登录
bot = Bot(cache_path=True)

bot.groups(update=True, contact_only=False)
allGroups = bot.groups()                    #获取所有群聊名
allFriends = bot.friends(update=True)       #获取所有好友的昵称

dateTime = None
friends = []
nickname = []
groups = []
groupNickName = []

msg = '输入要发送的内容。----for test----'


def myFriends():
    '''获取要发送信息的好友昵称，添加到friends列表中'''

    # 添加需要接收消息的人的昵称，注意是写的是微信昵称，非备注名，也不是微信号，可添加多个
    global nickname
    nickname = ['fangyueyan啦啦啦','TonyMr','向春晓','向春晓dfsdfsaf']
    for i in nickname:
        try:
            if bot.friends().search(i)[0] in allFriends:
                friends.append(bot.friends().search(i)[0])
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 不在您的好友列表中，请检查下填写的昵称是否正确！"%i)
            print("%s 不在您的好友列表中，请检查下填写的昵称是否正确！"%i)


def group(groupName):
    '''获取匹配上的群聊名称，添加到groups列表中'''

    group = bot.groups().search(nick_name=groupName)  # 精确匹配群名
    #group = bot.groups().search('人')  # 模糊匹配
    print(group)
    for i in group:
        try:
            if i in allGroups:
                groups.append(i)
        except Exception:
            # 给 文件传输助手 发消息
            bot.file_helper.send("%s 请检查下填写的昵称是否正确！")
            print("请检查下填写的昵称是否正确！")
    print(groups)

def sendNews(flag,groups_or_friends):
    for friend in groups_or_friends:
        friend.send("----- for test -----")

    bot.file_helper.send("不在您的好友列表中，请检查下填写的昵称是否正确！")
    if flag == "True":
        t = Timer(5,sendNews,(flag,groups_or_friends))
        t.start()


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

group('兄弟')

# myFriends()
# sendNews("True",friends)



# def sendFriendNews(flag,groups_or_friends):
#     # #设置发送的内容,并送给指定的人
#     # for friend in friends:
#     #     friend.send(msg)
#     #     print("消息已发送，发送时间: %s" % dateTime)
#     bot.file_helper.send("不在您的好友列表中，请检查下填写的昵称是否正确！")
#     if flag == "True":
#         t = Timer(1,sendFriendNews,(flag,groups_or_friends))
#         t.start()


# def sendGroup():
#     for group in allGroups:
#         group.send("谢谢！！！")
#
# def sendAllFriendNews():
#     #发送给所有的人
#     for friend in allFriends:
#         friend.send(msg)
#         print("消息已发送，发送时间: %s" % dateTime)



# def timing(flag,func):
#     if flag == "True":
#         t = Timer(1, func)
#         t.start()



# def test():
#     timing("True",sendFriendNews)
#     while True:
#         time.sleep(1)
#
# def main():
#     test()
#
# main()



#
# def main():
#     set_time()
#     global dateTime
#     dateTime = datetime.datetime.now()
#
#
# if __name__ == "__main__":
#     #main()
#     pass

# bot.groups(update=True, contact_only=False)
# group = bot.groups().search('人')    #模糊匹配
# print(group)
#group.send("@all 各位，这个星期四之前把要报销车票发到我微信上，我调休不在公司，所以不要发到我邮箱，谢谢！！！")



#group2 = bot.groups().search(nick_name='家人')    #精确匹配群名
#print(group2)

