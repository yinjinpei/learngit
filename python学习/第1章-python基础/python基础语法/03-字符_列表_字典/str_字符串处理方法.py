#_*_ coding:utf-8 _*_

#find 正向查找，即从左到右查找
str = "hello world peter and peterName!!"


print(str.find("peter")) #查找字符串，找到时反回标记位置，找不到时返回-1
print(str.find("alex"))

#rfind 反向查找，即从右到左查找
print(str.rfind("peter"))

#index与rindex， 和find，rfind不同，找不到时程序会出现异常（程序崩溃）
print(str.index("peter"))
#print(str.rindex("alex"))


#count 统计个数
# mystr.count(str, start=0, end=len(mystr))

#isspace 如果 mystr 中只包含空格，则返回 True，否则返回 False.
str = "hello world peter and peterName!!"
mystr = " "
print(str.isspace())
print(mystr.isspace())