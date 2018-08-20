
############# 浅拷贝 ###############
a = [11,22,33]
b = a
print(id(a))
print(id(b))

a.append("b")
print(a)

#结果：[11, 22, 33, 'b']   b列表会跟着a改变而改变,a与b 指向同一个地址


############# 深拷贝 ###############
import copy
c = [11,22,33]
d = copy.deepcopy(c)
print(id(c))
print(id(d))

c.append("d")
print(d)

#结果：[11, 22, 33]   c列表不会跟着a改变而改变，c与d 分别指向不同的地址