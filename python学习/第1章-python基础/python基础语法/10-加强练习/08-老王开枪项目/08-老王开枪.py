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
            if self.hp > 0:
                return "%s剩余血量为：%d,他没有枪！！"%(self.name,self.hp)
            else:
                return '敌人 "%s" 已挂。。。。'%self.name

    def kou_ban_ji(self,diren):
        """让枪发射子弹去打敌人"""

        #枪.开火(敌人)
        self.gun.fire(diren)

    def diao_xue(self,sha_shang_li):
        self.hp -= sha_shang_li


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

    def fire(self,diren):
        """枪从弹夹中获取一发子弹，然后让子弹击去中敌人"""

        #1,先从弹夹中取子弹
        #弹夹.弹出一发子弹()
        zidan_temp = self.danjia.tanchu_zidan()

        #2,让这个子弹去伤害敌人
        #子弹.击中敌人(敌人)
        if zidan_temp:
            zidan_temp.dazhong(diren)
        else:
            return "弹夹中没有子弹了。。。。"

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

    def tanchu_zidan(self):
        """弹出最上面的颗子弹，即是最后安装上的那一颗子弹"""
        if self.zidan_list:
            return self.zidan_list.pop()
        else:
            return None

class Zidan(object):
    """子弹的类"""
    def __init__(self,sha_shang_li):
        self.sha_shang_li = sha_shang_li #这颗子弹的杀伤力

    def dazhong(self,diren):
        """伤害敌人,使敌人掉血"""

        #敌人.掉血（一颗子弹的伤害）
        diren.diao_xue(self.sha_shang_li)



def main():
    '''用来控制整个程序的流程'''

    zi_dan_sum = int(input("需要安装几颗子弹？ ："))
    while True:
        kanqiang_sum = int(input("需要击中老王多少枪？ ： "))
        if kanqiang_sum > zi_dan_sum:
            print("没有这么多子弹可射击，射击次数必须小于子弹数量！！")
            continue
        else:
            break

    #1，创建开枪的人的对象
    laowang = Person("老王")
    #print("开枪人的名字：%s"%laowang.name)  #for test

    #2，创建一把枪对象
    ak47 = Gun("Ak47")
    #print("枪的名字：%s"%ak47.name)     #for test

    #3，创建弹夹对象
    dan_jia = Danjia(20)

    #4，创建一些子弹对象
    #zi_dan_sum = int(input("需要安装几颗子弹？ ："))
    for i in range(zi_dan_sum):
        zi_dan = Zidan(10)

        #5，老王把子弹安装到弹夹中
        #老王.安装子弹到弹夹中(弹夹，子弹)
        laowang.anzhuang_zidan(dan_jia,zi_dan)

    #6, 老王把弹夹安装到枪中
    #老王.安装弹夹到枪里(枪，弹夹)
    laowang.anzhuang_danjia(ak47,dan_jia)

    #test:测试弹夹中的信息
    #print(dan_jia) #for test

    # test:测试枪中的信息
    #print(ak47)    #for test

    #7，老王拿枪
    #老王.开枪击中敌人(枪)
    laowang.naqiang(ak47)

    #test:测试老王对象信息
    print(laowang)


    #8，创建敌人对象
    laosong = Person("老宋")
    #print(laosong)  #for test

    #9，老王开枪打敌人
    #老王.扣扳机(老宋)   #第调用一次即开枪一次

    #kanqiang_sum = int(input("需要击中老王多少枪？ ： "))
    i = 1
    while i <= kanqiang_sum:
        laowang.kou_ban_ji(laosong)
        i += 1

    print(laosong)

if __name__ == "__main__":
    main()