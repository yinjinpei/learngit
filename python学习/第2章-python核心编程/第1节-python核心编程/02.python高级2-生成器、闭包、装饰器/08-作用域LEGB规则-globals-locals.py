#-*- coding:utf-8 -*-
#author:YJ沛


'''
LEGB规则：locals -->enclosing function -->globals -->builtins
        局部变量     外部嵌套函数的命名空间  全局变量    内践（默认的拥有的）

locals() 打印局部变量

globals() 打印全局变量

'''

c = 80
d = 90

def test():
    a = 100
    b = 100
    print(locals())

print(globals())
test()


#查看内践（默认的拥有的）方法:
print(dir(__builtins__))

