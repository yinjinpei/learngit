class Person(object):
    """人的类"""
    def __init__(self,name):
        self.name = name

    def anzhuang_zidan(self,danjia_temp,zidan_temp):
        """把子弹安装到弹夹中"""

        #弹夹.保存子弹(子弹)
        danjia_temp.baocun_zidan(zidan_temp)

    def anzhuang_danjia(self,gun_temp,danjia_temp):
        """把弹夹安装到枪中"""

        #枪.保存弹夹(弹夹)
        gun_temp.baocun_danjia(danjia_temp)


class Gun(object):
    """枪的类"""
    def __init__(self,name):
        self.name = name    #用来记录枪的类型
        self.danjia = None  #用来记录弹夹的引用

    def baocun_danjia(self,danjia_temp):
        self.danjia = danjia_temp


class Danjia(object):
    """弹夹的类"""
    def __init__(self,max_num):
        self.max_num = max_num  #保存弹夹的最大容量
        self.zidan_list = []    #用来记录所有子弹的引用

    def baocun_zidan(self,zidan_temp):
        """将这颗子弹保存"""
        self.zidan_list.append(zidan_temp)
        pass

class Zidan(object):
    """子弹的类"""
    def __init__(self,sha_shang_li):
        self.sha_shang_li = sha_shang_li #这颗子弹的杀伤力


def main():
    '''用来控制整个程序的流程'''
    pass

    #1，创建开枪的人的对象
    laowang = Person("老王")
    print("开枪人的名字：%s"%laowang.name)

    #2，创建一把枪对象
    ak47 = Gun("Ak47")
    print("枪的名字：%s"%ak47.name)

    #3，创建弹夹对象
    dan_jia = Danjia(20)

    #4，创建一些子弹对象
    zi_dan = Zidan(10)

    #5，老王把子弹安装到弹夹中
    #老王.安装子弹到弹夹中(弹夹，子弹)
    laowang.anzhuang_zidan(dan_jia,zi_dan)

    #6, 老王把弹夹安装到枪中
    #老王.安装弹夹到枪里(枪，弹夹)
    laowang.anzhuang_danjia(ak47,dan_jia)

    #7，老王拿枪

    #8，创建敌人对象

    #9，老王开枪打敌人


if __name__ == "__main__":
    main()