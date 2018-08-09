#_*_ coding:utf-8 _*_

nameList = [] #定义一个空列表，用来储存所有个人信息

def printInfo():
    '''只打印提示信息'''
    print("="*30)
    print("  名片系统v1.0.0")
    print("添加一个名字请输入：1")
    print("删除一个名字请输入：2")
    print("修改一个名字请输入：3")
    print("查询一个名字请输入：4")
    print("查询所有名片请输入：5")
    print("保存个人信息请输入：6")
    print("退出系统   请输入: 7")
    print("="*30)

def suerInfo():
    '''用户输入个人信息模块'''
    userDict = {}  # 定义一个空字典，用来储存个人信息
    userDict["Name"] = input("请输入你的名字: ")
    userDict["Age"]  = int(input("请输入你的年龄: "))
    userDict["Sex"]  = input("请输入你的性别: ")
    userDict["QQ"]   = int(input("请输入你QQ: "))
    userDict["PhoneNum"] = int(input("请输入你的手机号: "))
    userDict["Addr"] = input("请输入你的住址: ")

    nameList.append(userDict)  # 把个人信息存入列表
    print("您添加的个人信息如下：\n姓名\t\t年龄\t性别\tQQ\t\t\t手机号\t\t 住址")
    print("%s\t%d\t%s\t%d\t%d\t%s" % (
    userDict["Name"], userDict["Age"], userDict["Sex"], userDict["QQ"], userDict["PhoneNum"], userDict["Addr"]))
    #print(nameList) #for test

def find_name():
    '''查询功能模块'''
    print('''查询类型：
        姓名：1
        年龄：2
        性别：3
        手机：4
        住址：5        
                ''')
    findTmpNum = int(input("请输入你要查询的类型："))

    # 查询名字模块
    if findTmpNum == 1:

        findName     = input("请输入你要查询的姓名：")
        findNameFlag = 0  # 查询标记，找到为1，找不到为0
        for tmpDict in nameList:  # 把字典从列表中单独取出来成字典
            if tmpDict["Name"] == findName:
                print("所有个人信息如下：\n姓名\t\t年龄\t性别\tQQ\t\t\t手机号\t\t住址")
                print("%s\t%d\t%s\t%d\t%d\t%s" % (
                tmpDict["Name"], tmpDict["Age"], tmpDict["Sex"], tmpDict["QQ"], tmpDict["PhoneNum"], tmpDict["Addr"]))
                findNameFlag = 1

        if findNameFlag == 0:
            print("查无此人！！！")

def showAllInfo():
    '''查询所有名片'''
    print("所有个人信息如下：\n姓名\t\t年龄\t性别\tQQ\t\t\t手机号\t\t住址")
    for tmpe in nameList:
        print("%s\t%d\t%s\t%d\t%d\t%s" % (
        tmpe["Name"], tmpe["Age"], tmpe["Sex"], tmpe["QQ"], tmpe["PhoneNum"], tmpe["Addr"]))

def save_2_infos():
    f = open("07-name_infos.data","w")
    f.write(str(nameList))
    f.close()


def main ():
    '''控制主程序的核心模块'''

    try:    #如何加载的文件不存在则不做异常处理，而是忽略，使程序断续往下走
        global nameList
        f = open("07-name_infos.data")
        nameList = eval(f.read())   #把上次保存的文件内容加载到程序中
        f.close()
    except:
        pass

    printInfo() #打印提示信息

    while True:

        userNum = int(input("请输入你要想的功能: "))

        if   userNum == 1:
            suerInfo()  #输入用户个人信息

        elif userNum == 2:
            pass        #删除功能

        elif userNum == 3:
            pass        #修改功能

        elif userNum == 4:
            find_name() #查询用户个人信息

        elif userNum == 5:
            showAllInfo()  #查询所有人的个人信息

        elif userNum == 6:
            save_2_infos()  #保存个人信息到本地，下次程序启动可以查看以前记录

        elif userNum == 7:
            break       #退出系统

        else:
            print("输入有误，请重新输入！！")

if __name__ == "__main__":
    main()  #主程序