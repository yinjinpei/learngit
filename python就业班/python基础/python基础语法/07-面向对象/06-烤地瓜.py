class SweetPotato():

    def __init__(self):
        self.stat = "生的"
        self.leve = 0
        self.addiments = [] #添加的调味料

    def __str__(self):
        return "地瓜现状：%s  添加的调味料有：%s"%(self.stat,self.addiments)

    def cook(self,cookTime):
        self.leve += cookTime

        if self.leve >= 0 and self.leve < 3:
            self.stat="煮了%d分钟，煮得还不够久，还是生的！"%self.leve
        elif self.leve >= 3 and self.leve < 5:
            self.stat ="煮了%d分钟，煮得差不多了，现在是半生半熟！"%self.leve
        elif self.leve >= 5 and self.leve < 8:
            self.stat ="煮了%d分钟，煮熟了，可以吃了！"%self.leve
        elif self.leve >= 8:
            self.stat ="煮了%d分钟，兄弟，煮太远了，都成炭了！！"%self.leve

    def addiment(self,listName):
        self.addiments.append(listName)

her = SweetPotato()
i = 0
list = ["清油","烧烤汁","胡椒粉","盐","醋","葱","番茄酱"] #for test

while i < 7:
    her.cook(1)
    her.addiment(list[i])
    print(her)
    i +=1

