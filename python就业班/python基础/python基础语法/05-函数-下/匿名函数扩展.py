
def test(a,b,func):
    result = func(a,b)
    return result

func_new = input("请输入一个函数: ")   #输入：lambda x,y:x+y
func_new =eval(func_new)    #eval函数就是实现list、dict、tuple与str之间的转化，相当于把""符号去除
num = test(11,22,func_new)
print(num)

#执行时输入：lambda x,y:x+y


