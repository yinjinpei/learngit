#-*- coding:utf-8 -*-
#author:YJ沛

#比如给一个页面字体装饰，加粗和加大

#定义函数，完成包裹数据，功能是字体加粗
def makeBold(fn):
    def wrapped():
        print("----- 1 ------")
        return "<b>" + fn() + "</b>"
    return wrapped

#功能是字体加大
def makeItalic(fn):
    def wrapped():
        print("----- 2 ------")
        return "<i>" + fn() + "</i>"
    return wrapped

@makeBold
@makeItalic
def test():
    print("------ test -------")
    return "Hello Word!"

ret = test()
print(ret)

'''
执行结果：
----- 1 ------
----- 2 ------
------ test -------
<b><i>Hello Word!</i></b>

'''