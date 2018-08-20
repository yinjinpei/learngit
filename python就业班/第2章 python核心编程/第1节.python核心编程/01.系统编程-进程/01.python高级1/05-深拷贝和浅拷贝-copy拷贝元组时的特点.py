import copy

a = [11,22,33]
b = [44,55,66]
c = (a,b)

a.append("aa")
print(c)


d = copy.copy(c)    #copy模块中的copy功能会自动判断是可变还是不可变类型，
b.append("bb")

print(id(c))    #51512184
print(id(d))    #51512184 和上面一样，元组是不可变类型，指向地址一样
print(d)


e = copy.deepcopy(c)
a.append("aa-bb")

print(id(c))    #51512184
print(id(e))    #51473864  一样
print(e)


