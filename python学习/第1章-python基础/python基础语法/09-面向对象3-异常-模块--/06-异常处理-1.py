

# 变量异常：NameError
# 文件不存在异常：FileNotFoundError

#print(jj) for test

try:
    open("xxx.txt")
    #print(num)     #for test
    print("----------1------------")

except NameError:   #变量异常处理
    print("变量不存在。。。。")

except FileNotFoundError:   #文件不存在异常处理
    print("文件不存在，请检查下！！！！")



print("-----2--------")
