#-*- coding:utf-8 -*-

def user():
    userName=input("你的名字：")
    userAge=int(input("你的年龄："))
    userAddr=input("你居住的所在地：")

    return userName,userAge,userAddr

def printUser(name,age,addr):
    print("名字：%s \n年龄：%d\n住址：%s"%(name,age,addr))


resule=user()
printUser(resule[0],resule[1],resule[2])