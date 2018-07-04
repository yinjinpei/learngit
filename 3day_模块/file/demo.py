#_*_ coding:utf-8 _*_


#print('yes',__name__)

def Foo():
    name = 'peter'
    print('%s上山打老虎了！' % name)


#限制非__main__不得直接调用模块直接执行函数
if __name__ == '__main__':
    Foo()
else:
    print('非主程序，不得执行！')
