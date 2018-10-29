#_*_ coding:utf-8 _*_

#打印信息
print("="*30)
print("添加一个名字请输入：1")
print("删除一个名字请输入：2")
print("修改一个名字请输入：3")
print("查询一个名字请输入：4")
print("退出系统   请输入：5")
print("="*30)

nameList = [] #定义储存名字的列表

while True:
    #功能
    userNum = int(input("请输入你要想的功能: "))

    if userNum == 1:
        #添加功能
        newName = input("请输入要添加的名字: ")
        nameList.append(newName)
        print(nameList)

    elif userNum == 2:
        #删除功能
        delName = input("请输入要删除的名字: ")
        if delName in nameList:
            nameList.remove(delName)    #不考虑有重复名字，默认删除最先找到的（从左到右到）
            print("删除成功，%s已被删除！" % delName)
        else:
            print("删除失败，查无此人，%s可能是假的名字！" % delName)

    elif userNum == 3:
        #修改功能
        modifyName = input("请输入要修改的名字: ")
        if modifyName in nameList:
            newModifyName = input("请输入新的名字: ")
            modifyNameIndex = nameList.index(modifyName)
            nameList[modifyNameIndex] = newModifyName
            print("修改成功，%s已被修改成%s！" %
                  (modifyName,newModifyName))
        else:
            print("修改失败，查无此人，%s可能是假的名字！" % modifyName)

    elif userNum == 4:
        #查询功能
        findName = input("请输入要添查看的名字: ")
        if findName in nameList:
            print("找到了，%s 此人真实存在！"%findName)
        else:
            print("查无此人，%s可能是假的名字！" %findName)

    elif userNum == 5:
        #退出系统
        break
    else:
        print("输入有误，请重新输入！！")