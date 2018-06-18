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

print ('''
Personal information of %s:
        Name: %s
        Age:  %s   
        Job:  %s
     Salary:  %s
--------------------------      
''' % (name,name,age,job,salary))

