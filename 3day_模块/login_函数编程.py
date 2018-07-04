 #_*_ coding:utf-8 _*_


###################  传参一个 ######################
# 调用login.py模块
from Foo import login

login.name('peter')
login.name('alex')
login.name('lisi')

if __name__ == '__main__':
    #user = input('请输入用户名：')
    user = 'peter'
    login.login(user)
    res = login.login(user)

    if res == '登录成功':
        print('登录成功！！')
        login.detail(user)
    else:
        print('登录失败！！')
        print('破产了，没资金！')

###################  传参多个 ######################
#为了看得简单，不调用模块
def foo(name,action='干嘛了？',number ='队员'):
    print(name,action,number)

foo('peter','去吃饭了！','总裁')
foo('alex','去锻炼了！')
foo('jinpei','去打老虎了！',number='精英')
foo(name='xxx',action='去碰瓷了',number='没有这样的朋友')

###################  传参列表 ######################

def show(*args):
    for i in args:
         print(i)

#方法一
show(['peter','17岁','男'])

#方法二
user_list = ['peter','17岁','男']
show(*user_list)

###################  传参字典 ######################

def show(**kwargs):
    for i in kwargs:
        print(i,kwargs[i])

#方法一：
show(name='peter',age='17',sex='男')

#方法二:
user_dict = {'name':'peter','age':'17','sex':'男'}
show(**user_dict)

###################################################