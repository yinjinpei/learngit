#导入模块方法一
import msgnew
msgnew.test1()

#导入模块方法二
from msgnew import test1
test1()

#导入模块方法三 ,此方法不建义用，如有函数名重复，前者会被后者覆盖
from msgnew import *
test1()

#####################  02-模块中的__all__的作用  #####################
from msgnew_two import *
test1()

a = test2()
print(a)

test3 = Test3()
test3.test_print()

print(number)