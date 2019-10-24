
class A(object):
    def __init__(self):
        self.abc = 123


class B(object):
    # def __init__(self):
    #     self.abc = 222
    pass

class C(A):
    def __init__(self):
        self.abc =333

class D(B,C):
    pass



d = D()
print(d.abc)





import sys
import time
def progress_bar(total):
   """
   进度条效果
   """
   # 获取标准输出
   _output = sys.stdout
   # 通过参数决定你的进度条总量是多少
   for count in range(0, total + 1):
       # 这里的second只是作为工作量的一种代替
       # 这里应该是有你的主程序,main()
       _second = 0.1
       # 模拟业务的消耗时间
       time.sleep(_second)
       # 输出进度条
       _output.write(f'\rcomplete percent:{count:.0f}')
   # 将标准输出一次性刷新
   _output.flush()
progress_bar(100)