
#相互交换值
a = 4
b = 5

#方法一
c = 0 #定义第三个变量
c = a
a = b
b = c
print("a=%d,b=%d"%(a,b))

#方法二：
a = 4
b = 5
a = a+b
b=a-b
a=a-b
print("a=%d,b=%d"%(a,b))

#方法三:python独有的方法
a = 4
b = 5
a,b=b,a
print("a=%d,b=%d"%(a,b))