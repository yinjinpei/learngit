#  # coding:utf-8
# # author:YJ沛
#
#
#
#
# '''
# 【for语句/while语句】循环提示用户输入一个整型数字n（n代表后续需要输入整型数的数量），将n个整型数加起来并输出，
# 如果输入的是非整型数则提示当前的输入非法需要重新输入数值，如果输入‘n=0’代表退出程序，否则继续提示用户输入新的n
# '''
#
# Number = []
#
# def main():
#
#     while True:
#         try:
#             number = int(input("请输入一整数: "))
#         except:
#             print("输入格式不正确，请重新输入！")
#         else:
#             if number == 0:
#                 break
#             else:
#                 Number.append(number)
#
#     sum = 0
#     for i in Number:
#         sum += i
#
#     print("总和为： %d "% sum)
#
#
# if __name__ == "__main__":
#     main()
#
#
#
# '''1!+3!+5!+7!.....+n!，用python怎么写'''
#
# Number = int(input("输入一个正整数："))
#
# # 存放所有奇数
# NumberList = []
#
# # 存放每个奇数阶乘后的结果
# SumList = []
#
# sum = 0
#
# for i in range(1, Number + 1):
#     '''获取Number范围内的所有奇数'''
#     if i%2 == 0:
#         continue
#     else:
#         NumberList.append(i)
#
# for i in NumberList:
#     '''计算每个奇数阶乘后的结果'''
#     s = 1
#     for j in range(1, i + 1):
#         s *= j
#     SumList.append(s)
#
# for i in SumList:
#     '''计算总和'''
#     sum += i
#
# print(NumberList)   # for test
# print(SumList)   # for test
# print("总和：%d " % sum)
#
#
#
#

#
# f = open("content", "r")
# data = f.read()
# print(data)
#

# 2.求1--100之间可以被7整除的数的个数
# sum = 0
# for i in range(1,101):
#     if 0 == i % 7:
#         print(i)
#         sum += i
# print(sum)


# 5.计算1到100以内能被7或者3整除但不能同时被这两者整除的数的个数。
# i = 3
# sum = 0
# while i <= 100:
#     if 0 == i%3 or 0 == i%7:
#         if i % 21 == 0:
#             i += 1
#             continue
#         else:
#             print(i)
#             sum += 1
#     else:
#         pass
#     i += 1
# print("总个数：%d" % sum)



# 6.计算1到500以内能被7整除但不是偶数的数的个数。
i = 1
sum = 0
while True:
    if i*7 >= 500:
        break
    elif i * 7 % 2 != 0:
        print(i*7)
        i += 1
        sum += 1
    else:
        i += 1
print("总个数：%d" % sum)



# 7.计算从1到1000以内所有能同时被3，5和7整除的数的和并输出
# 方法一
i = 1
sum = 0
while i <= 1000:
    if i % 3 == 0:
        if i % 5 == 0:
            if i % 7 == 0:
                print(i)
                sum += i
    i += 1
print(sum)

print("-"*10)

# 方法二
i = 1
sum = 0
a = 3*5*7
while i <= 1000:
    if i % a == 0:
        print(i)
        sum += i
    i+=1
print(sum)

print("-"*10)

# 方法三
i = 1
sum = 0
while True:
    if i*105 >= 1000:
        break
    else:
        print(i*105)
        sum += i*105
        i += 1
print(sum)


# 1.3000米长的绳子，每天减一半。问多少天这个绳子会小于5米？不考虑小数
long = 3000
day_num = 0
while True:
    if long/2 > 5:
        print(long)
        long /= 2
        day_num += 1
    else:
        print(long)
        print(day_num)
        break


# 例如： 153 = 1（3） + 5（3）+ 3（3） = 1+125+27 = 153
i = 100
while True:
    if i > 1000:
        break
    else:
        j = 0
        for k in str(i):
            j += int(k)**3
        if j == int(i):
            print("水仙花数字： %d " % i )
        i += 1


# 3.五位数中，对称的数称为回文数，打印所有的回文数并计算个数
# 10000 - 99999
i = 10000
sum = 0
while True:
    if i > 99999:
        break
    else:
        if str(i)[0] == str(i)[4]:
            if str(i)[1] == str(i)[3]:
                print(i)
                sum += 1
        i += 1
print("回文数总个数: %d" % sum)


# 1.输出9行内容，，第1行输出1，第2行输出12，第3行输出123，以此类推，第9行输出123456789
for i in range(1,10):
    for i in range(1,i+1):
        print(i, end="")
    print("")


'''
2.打印图形

		*
       ***
      *****
     *******
'''
i = 1
k = 4   #打印行数
while i <= k:
    print(" "*(k-i),end="")
    print("*" * (2 * i - 1))
    i += 1


'''
3.打印实心菱形
     *
    ***
   *****
  *******
   *****
    ***
     *
'''







'''
4.打印空心菱形

     *
    * *
   *   *
  *     *
   *   *
    * *
     *
'''

import requests