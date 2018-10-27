#-*- coding:utf-8 -*-
import sys
from imp import *   #重加载模块reload所用的模块
import test

print(sys.path)  #显示当前搜索的模块路径

sys.path.append("../") #添加搜索模块路径

print(sys.path)

reload(test)    #重加载模块



'''
 ========= 循环导入问题 ===========
a.py:
    from b import b
    
    print ("-----a ------")


b.py:
    from a import a
    
    print ("-----b ------")

==================================

=========== 解决方法 ==============
#a,b都不导入模块，新建c.py:
    from a import a
    from b import b
    a()
    b()

'''