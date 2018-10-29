

f = open("filedir/test.py","w+")
f.write("yinjinpei\npeter\nalex")
f.seek(0)
stu=f.read()
print(stu)
f.close()


file =open("filedir/test.py","r")
str=file.read()
print(str)
file.close()
