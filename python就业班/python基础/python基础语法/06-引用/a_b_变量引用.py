a = 100
b = a
c = 200
d = 200
print("a=%d,b=%d"%(id(a),id(b)))
print("c=%d,d=%d"%(id(c),id(d)))


#列表
A=[1,2,3]
B=A
C=[1,2,3]
D=[1,2,3]
print("A=%d,B=%d"%(id(A),id(B)))
print("C=%d,D=%d"%(id(C),id(D)))
A.append(4)
C.append(4)
print("A=%d,B=%d"%(id(A),id(B)))
print("C=%d,D=%d"%(id(C),id(D)))
