a=100
def test(num):
    num+=num
    print(num)
    return num
test(a)
print(a)
print("-"*30+"该死的分割线"+"-"*30)

a=[100]
def test(num):
    num+=num    #与 num = num+num 不一样，这里是修改可变型的变量（列表）
    print(num)
    return num
test(a)
print(a``print("-"*30+"该死的分割线"+"-"*30)

a=[100]
def test(num):
    num = num+num   #与 num+=num  不一样，这里是新变量num赋值
    print(num)
    return num
test(a)
print(a)