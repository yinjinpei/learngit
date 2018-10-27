class Person(object):
    """人的类"""
    def __init__(self,name):
        self.name = name
        self.gun = None #用来保存枪对象的引用
        self.hp = 100   #血量

    def anzhuang_zidan(self,danjia_temp,zidan_temp):
        """把子弹安装到弹夹中"""

        #弹夹.保存子弹(子弹)
        danjia_temp.baocun_zidan(zidan_temp)

    def anzhuang_danjia(self,gun_temp,danjia_temp):
        """把弹夹安装到枪中"""

        #枪.保存弹夹(弹夹)
        gun_temp.baocun_danjia(danjia_temp)

    def naqiang(self,gun_temp):
        """拿起一把枪"""
        self.gun = gun_temp

    def __str__(self):
        if self.gun:
            return "%s血量为：%d,他有枪！！ %s "%(self.name,self.hp,self.gun)
        else:
            return "%s血量为：%d,他没有有枪！！"%(self.name,self.hp)

class Gun(object):
    """枪的类"""
    def __init__(self,name):
        self.name = name    #用来记录枪的类型
        self.danjia = None  #用来记录弹夹对象的引用

    def baocun_danjia(self,danjia_temp):
        """用一个属性来保存这个弹夹对象的引用"""
        self.danjia = danjia_temp

    def __str__(self):
        if self.danjia:
            return "枪的信息为：%s, %s"%(self.name,self.danjia)
        else:
            return "枪的信息为：%s, 这把枪中没有弹夹！"%self.name

class Danjia(object):
    """弹夹的类"""
    def __init__(self,max_num):
        self.max_num = max_num  #保存弹夹的最大容量
        self.zidan_list = []    #用来记录所有子弹对象的引用

    def baocun_zidan(self,zidan_temp):
        """将这颗子弹保存"""
        self.zidan_list.append(zidan_temp)

    def __str__(self):
        return "弹夹的信息为:%d/%d"%(len(self.zidan_list),self.max_num)

class Zidan(object):
    """子弹的类"""
    def __init__(self,sha_shang_li):
        self.sha_shang_li = sha_shang_li #这颗子弹的杀伤力


def main():
    '''用来控制整个程序的流程'''

    #1，创建开枪的人的对象
    laowang = Person("老王")
    print("开枪人的名字：%s"%laowang.name)

    #2，创建一把枪对象
    ak47 = Gun("Ak47")
    print("枪的名字：%s"%ak47.name)

    #3，创建弹夹对象
    dan_jia = Danjia(20)

    #4，创建一些子弹对象
    for i in range(15):
        zi_dan = Zidan(10)

        #5，老王把子弹安装到弹夹中
        #老王.安装子弹到弹夹中(弹夹，子弹)
        laowang.anzhuang_zidan(dan_jia,zi_dan)

    #6, 老王把弹夹安装到枪中
    #老王.安装弹夹到枪里(枪，弹夹)
    laowang.anzhuang_danjia(ak47,dan_jia)

    #test:测试弹夹中的信息
    print(dan_jia)

    # test:测试枪中的信息
    print(ak47)

    #7，老王拿枪
    #老王.开枪击中敌人(枪)
    laowang.naqiang(ak47)

    #test:测试老王对象信息
    print(laowang)


    #8，创建敌人对象
    laosong = Person("老宋")
    print(laosong)

    #9，老王开枪打敌人


if __name__ == "__main__":
    main()