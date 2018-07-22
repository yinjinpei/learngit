#_*_ coding:utf-8 _*_

'''
注释模块，与 __doc__ 配合使用！

'''
'''
普通注释，非模块！
'''


from file import demo

demo.Foo()

if  __name__ == '__main__':
    print('index',__name__)

print(__file__)     #打印当前脚本路径
print(__doc__)      #打印注释模块内容





