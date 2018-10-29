

# 变量异常：NameError
# 文件不存在异常：FileNotFoundError
#所有异常：Exception
#无论是否会产生异常都执行:finally

try:
    #b = 11/0
    #open("xxx.txt")
    #print(num)     #for test
    print("----------1------------")

except (NameError,FileNotFoundError) as a:   #a相当为异常信息的别名
    print(a)
    print("变量或文件不存在，请检查下！！！！")
except Exception as ret:
    print(ret)
    print("如果用了Exception，那么意味着只要上面的except没有捕获到异常，这个except一定会捕获到")

else:
    print("没有异常才会执行的功能")

finally:
    print("无论是否会产生异常都执行!")



print("-----2--------")
