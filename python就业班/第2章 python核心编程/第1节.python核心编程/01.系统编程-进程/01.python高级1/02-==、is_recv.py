# ==：判断两个值是否相等
# is: 判断两个引用是否是同一个

a = [1,2,3]
b = [1,2,3]
c = a

print(id(a))
print(id(b))
print(id(c))


if a == b:     #True
    print("True")
else:
    print("False")


if a is b:      #False
    print("True")
else:
    print("False")


if a == c:      #True
    print("True")
else:
    print("False")


if a is c:      #True
    print("True")
else:
    print("False")
