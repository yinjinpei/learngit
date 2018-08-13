a = [11,22,33,44,55,66]
b = []
for i in a:
    if i ==33 or i==44:
        b.append(i)

for i in b:
    a.remove(i)

print(a)