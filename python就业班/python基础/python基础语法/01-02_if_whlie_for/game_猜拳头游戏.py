#_*_ coding:utf-8 _*_
import random


userNumber = int(input("1拳头，2剪刀，3布  你想出的是："))

#电脑随机获取1-3
computer = random.randint(1,3)

if (userNumber==1 and computer==2) or (userNumber==2 and computer==3) or (userNumber==3 and computer==1):
    print("你真聪明，这100万是你的了，拿走！")
elif userNumber==computer:
    print("平局，不服，再来一次！！")
else:
    print("竟然输了，不科学，再来，决战到天亮！！")