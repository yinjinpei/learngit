

'''
    f.seek(value1,value2)  value1为偏移量，可以省略，value2为开始位置
    f.tell  显示当前光标位置
'''

f = open("filedir/test.py")
sign1=f.seek(2)
sign2=f.read()
sign3=f.tell()
print(sign1,sign3,sign2)

f.close()
