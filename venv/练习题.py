# coding:utf-8
# author:YJ沛




'''
【for语句/while语句】循环提示用户输入一个整型数字n（n代表后续需要输入整型数的数量），将n个整型数加起来并输出，
如果输入的是非整型数则提示当前的输入非法需要重新输入数值，如果输入‘n=0’代表退出程序，否则继续提示用户输入新的n
'''

Number = []

def main():

    while True:
        try:
            number = int(input("请输入一整数: "))
        except:
            print("输入格式不正确，请重新输入！")
        else:
            if number == 0:
                break
            else:
                Number.append(number)

    sum = 0
    for i in Number:
        sum += i

    print("总和为： %d "% sum)


if __name__ == "__main__":
    main()



'''1!+3!+5!+7!.....+n!，用python怎么写'''

Number = int(input("输入一个正整数："))

# 存放所有奇数
NumberList = []

# 存放每个奇数阶乘后的结果
SumList = []

sum = 0

for i in range(1, Number + 1):
    '''获取Number范围内的所有奇数'''
    if i%2 == 0:
        continue
    else:
        NumberList.append(i)

for i in NumberList:
    '''计算每个奇数阶乘后的结果'''
    s = 1
    for j in range(1, i + 1):
        s *= j
    SumList.append(s)

for i in SumList:
    '''计算总和'''
    sum += i

print(NumberList)   # for test
print(SumList)   # for test
print("总和：%d " % sum)




