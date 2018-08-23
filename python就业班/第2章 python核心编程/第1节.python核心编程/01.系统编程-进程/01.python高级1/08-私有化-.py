#-*- coding:utf-8 -*-
#author:YJ沛

#-*- coding:utf-8 -*-
#author:YJ沛

#导入方法一
from test import *
print(num)
#print(_num)    #私有属性,  使用“from test import * ”导入方式调用不了
#print(__num)    #私有属性,使用“from test import * ”导入方式调用不了


#导入方法二
import test
print(test.num)
print(test._num2)       #私有属性，使用“import test ”导入方式可以调用
print(test.__num3)      #私有属性，使用“import test ”导入方式可以调用