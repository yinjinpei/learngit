

# 变量异常：NameError
# 文件不存在异常：FileNotFoundError



try:
    open("xxx.txt")
    print(num)     #for test
    print("----------1------------")

except (NameError,FileNotFoundError):   #多种异常处理
    print("变量或文件不存在，请检查下！！！！")


print("-----2--------")
