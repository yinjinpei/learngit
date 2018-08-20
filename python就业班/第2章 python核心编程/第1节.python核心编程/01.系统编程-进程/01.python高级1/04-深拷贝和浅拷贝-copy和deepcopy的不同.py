import copy

#------- copy.copy --------
a = [11,22,33]
b = [44,55,66]
c = [a,b]

d = copy.copy(c)    #也属于浅拷贝,但指向地址是新的
print(id(c))
print(id(d))
b.append("bb")  #影响 d列表
c.append("cc")  #不影响 d列表

print("c列表：",c)     #结果：c列表： [[11, 22, 33], [44, 55, 66, 'bb'], 'cc']
print("d列表：",d)     #结果：d列表： [[11, 22, 33], [44, 55, 66, 'bb']]


#------- copy.deepcopy --------
a = [11,22,33]
b = [44,55,66]
c = [a,b]

f = copy.deepcopy(c)
a.append("deep")

print(f)
print(c)