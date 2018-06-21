#!user/bin/env python
#_*_ coding:utf-8 _*_



name = input('Plesase input your name:')
while True:
    try:
        age = int(input('Plesase input your age:'))
        break
    except ValueError:
        print('ERROR: Value of initial position must be int number!')

job = input('Plesase input your job:')
salary = input('Plesase input your salary:')

if age > 40:
    msg = 'You are too fucking old!'
elif age >30:
    msg = '你差不多老了！'
else:
    msg = 'You are so young !!'

print ('''
Personal information of %s:
        Name: %s
        Age:  %s   
        Job:  %s
     Salary:  %s
--------------------------
%s      
''' % (name,name,age,job,salary,msg))

