import copy

print("#------- copy.copy --------")
a = [11,22,33]
b = [44,55,66]
c = [a,b]

d = copy.copy(c)    #也属于浅拷贝,指向地址是新的，但d列表里面a和b指向的地址和上面的a和b是一样的
print(id(c))
print(id(d))
b.append("bb")  #影响 d列表
c.append("cc")  #不影响 d列表

print("c列表：",c)     #结果：c列表： [[11, 22, 33], [44, 55, 66, 'bb'], 'cc']
print("d列表：",d)     #结果：d列表： [[11, 22, 33], [44, 55, 66, 'bb']]


print("#------- copy.deepcopy --------")
a = [11,22,33]
b = [44,55,66]
c = [a,b]

f = copy.deepcopy(c)   #深拷贝
a.append("deep")       #不影响 f列表

print("c列表：",c)     #结果: c列表： [[11, 22, 33, 'deep'], [44, 55, 66]]
print("f列表：",f)     #结果：f列表： [[11, 22, 33], [44, 55, 66]]
