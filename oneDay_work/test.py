#如何用python将变量及其值写入文本文件?



x=5
y=2
z=x+y
f=open('test.txt','a+')
f.write(str("x=")+str(x)+'\n')
f.write(str("y=")+str(y)+'\n')
f.write(str("z=")+str(z)+'\n')
f.close()