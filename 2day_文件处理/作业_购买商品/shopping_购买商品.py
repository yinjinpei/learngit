#_*_ coding:utf-8 _*_
'''
*****************************************************
 使用说明：让用户输入月薪工资金额，不断购买商品，直到钱不够为止

*****************************************************
'''

while True:
    try:
        Wage = float(input('请输入你的月薪收入金额：'))     #月薪工资
        break
    except ValueError:
        print('输入错误，请输入一个数字!!')

print('''
*********** 请按编号输入你要想买的商品 **************

1. Iphone X     ￥6999
2. 华为P20       ￥3788
3. 小米8         ￥2699
4. 小米笔记本pro  ￥5599
5. 九号平衡车     ￥1999
6. 空气净化器2s   ￥899
7. 小米AI音箱     ￥299
8. 小米路由器3C   ￥99
9. 新小米移动电源  ￥79
10.米家随身风扇    ￥19.9

************************************************
''')
Price        = [6999,3788,2699,5599,1999,899,299,99,79,19.9]    #商品对应价格列表
Commodity    = ['Iphone X','华为P20','小米8','小米笔记本pro','九号平衡车','空气净化器2S','小米AI音箱','小米路由器3C','新小米移动电源','米家随身风扇']
AllCommodity = []
Balance      = Wage      #余额
while Balance >= 19.9:   #判断剩余余额是否可以购买最低价格的商品

    while True:
        try:
            Number = int(input('''-------------------
请输入你要买的商品：'''))
            if Number >0 and Number <=10:         #判断输入编号是否正确
                break
            else:
                print('输入错误，请输入一个商品对应的编号!!')
                continue
        except ValueError:
            print('输入错误，请输入一个商品对应的编号!!')

    if Balance < int(Price[Number-1]):            #判断余额是否足够购买商品
        print('对不起，您的余额不足，无法购买此商品，请选择其它商品购买！！')
        continue

    AllCommodity.append(Commodity[Number-1])      #记录已购买的商品名，每购买一个商品将商品名追加到AllCommodity数组里
    Balance    = Balance - int(Price[Number-1])   #计算剩余余额
    print('''===================
您的余额为：%s''' % Balance)
    buy = input('是否继续购买商品? Y/N  ')
    if buy != 'y' and buy != 'Y':
        break
else:

    print('对不起，您的余额不足，无法购买任何商品，请发工资再来购买吧，谢谢惠顾！！')

print('''
==== 您的购买商品清单如下 ====
%s    
==========================
    一共支付金额：%s
    剩余总余额为：%s
''' % ('\n'.join(AllCommodity),Wage-Balance,Balance))

