'''
    pdb调试：
        l: list显示当前的代码
        n: next执行下一行
        c: continue继续执行，一次性执行到最后，相当于一步执行完程序
        b: break 添加断点，使用方法：设置断点b 7，查看断点：b+
        p: 打印一个变量的值
        a: 打印所有的形参数据
        s: step 进入到一个函数
        r: return 快速执行到函数的最后一行
        q: 退出调试
'''

def sum(a, b):
    result = a +b
    print(result)
    return  result

