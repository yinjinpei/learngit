
class Home:
    def __init__(self,new_area,new_info,new_addr):
        self.area = new_area
        self.info = new_info
        self.addr = new_addr
        self.contain_items = []

    def __str__(self):
        return "房子可用面积为：%d, 户型：%s, 地址：%s 床名：%s" % (self.area,self.info,self.addr,self.contain_items)

    def remain_area(self,items):    #获取床的属性
        #self.area -= items.area
        #self.contain_items.append(items.dict)
        self.area -= items.get_area()
        self.contain_items.append(items.get_bed_info())


class Bed:
    def __init__(self,new_name,new_area):
        self.name = new_name
        self.area = new_area

    def __str__(self):
        return "床的名字为：%s ,床的面积为：%d"%(self.name,self.area)

    def get_name(self):
        return self.name

    def get_area(self):
        return self.area

    def get_bed_info(self):
        self.dict = {"name": self.name, "area": self.area}
        return self.dict

tom = Home(130,"三房一厅","深圳")
bed = Bed("沛哥专用床",3)
bed1 = Bed("peter专用床",4)
bed2 = Bed("alex专用床",2)
tom.remain_area(bed)
tom.remain_area(bed1)
tom.remain_area(bed2)
print(tom)
