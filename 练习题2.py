# coding:utf-8
# author:YJ沛


'''
周长:C=2πr (r半径)
面积:S=πr²
半圆周长:C=πr+2r
半圆面积:S=πr²/2
'''


def main():
    print('''
选择：
    【1】 输入圆的半径，计算其的周长和面积
    【2】 输入圆的周长，计算其的半径和面积
    【3】 输入圆的面积，计算其的半径和周长
        ''')

    pi = 3.14

    while True:
        try:
            number = int(input("请选择功能[1 - 3]："))
            if number == 1:
                r = float(input("输入圆的半径："))
                c = 2 * pi * r
                s = pi * r**2
            elif number == 2:
                c = float(input("输入圆的周长："))
                r = c / (2 * pi)
                s = pi * r ** 2
            elif number == 3:
                s = float(input("输入圆的面积："))
                r = (s / pi)**00.5
                c = 2 * pi * r
            else:
                print("输入有误，请重新输入！")
                continue
        except BaseException:
            print("输入有误，请重新输入！")
        else:
            print("半径: %0.2f ,周长: %0.2f ,面积: %0.2f" %(round(r, 2),round(c, 2),round(s, 2)) )
            break


if __name__ == "__main__":
    main()
