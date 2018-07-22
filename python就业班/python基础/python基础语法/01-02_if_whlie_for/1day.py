#_*_ coding:utf-8 _*_

name = input("请输入你的名字：")
print("姓名：%s"  %name)

age = int(input("年龄："))
if age > 20:
    print("老油条了：%d"%age)
elif age <10:
    print("啥玩意")
else:
    print("小鲜肉：%d"%age)

