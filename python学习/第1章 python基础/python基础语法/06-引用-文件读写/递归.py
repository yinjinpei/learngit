
#阶乘
#4！，指4的阶乘，4*3*2*1
#5！，指5的阶乘，5*4*3*2*1

#实现方法一:
userNum = int(input("请输入一个数字："))   #5

i=1
result = 1
while i <= userNum:
    result = result * i
    i += 1


print(result)