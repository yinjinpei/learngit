
def test(a,b,func):
    result = func(a,b)
    return result

func_new = input("请输入一个函数: ")
func_new =eval(func_new)
num = test(11,22,func_new)
print(num)

#执行时输入：lambda x,y:x+y


