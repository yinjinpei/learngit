#_*_ coding:utf-8 _*_

i = 1
while i<=5:
    print("我爱你  "*i)
    i +=1

#嵌套循环
'''
#九九乘法
i = 1
while i <= 9:

    j = 1
    while j <= i:
        print("%d*%d=%d\t"%(i,j,i*j),end="")
        j+=1
    print("")
    i+=1
'''

#九九乘法，倒三角
i = 9
while i >= 1:
    j = 1
    while j <= i:
        print("%d*%d=%d\t"%(i,j,i*j),end="")
        j+=1
    print("")
    i-=1