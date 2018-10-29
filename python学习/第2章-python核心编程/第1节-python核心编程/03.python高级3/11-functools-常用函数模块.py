#-*- coding:utf-8 -*-
#author:YJ沛

'''
常用工具函数模块:

'''
import functools
#查看模块功能：
print(dir(functools))



# partial函数(偏函数),把一个函数的某些参数设置默认值，返回一个新的函数，调用这个新函数会更简单。
def showarg(*args,**kwargs):
    print(args)
    print(kwargs)

p1 = functools.partial(showarg, 1, 2, 3)
p1()
print('----------------------')
p1(4, 5, 6)
print('----------------------')
p1(a='python', b='itcast')

print('----------------------- 1 ----------------------------')

# wraps函数,使用装饰器时，有一些细节需要被注意。例如，被装饰后的函数其实已经是另外一个函数了（函数名等函数属性会发生改变）
def note(func):
    "note function"
    @functools.wraps(func)  #添加此行后查看test.__doc__则是test的帮忙文档，否则是wrapper的帮助文档
    def wrapper():
        '''wrapper function'''
        print('note something')
        return func()
    return wrapper

@note
def test():
    '''test function'''
    print('I am test')

test()
print(help(test))   #显示的是test函数帮忙文档
print(test.__doc__) #显示的是test函数帮忙文档

print('---------------------- 2 -----------------------------')

#不使用wraps函数
def note(func):
    "note function"
    def wrapper():
        '''wrapper function'''
        print('note something')
        return func()
    return wrapper

@note
def test():
    '''test function'''
    print('I am test')

test()
print(help(test))   #显示的是wrapper函数帮忙文档
print(test.__doc__) #显示的是wrapper函数帮忙文档