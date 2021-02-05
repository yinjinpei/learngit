#-*- coding:utf-8 -*-


movieName = ['加勒比海盗', '骇客帝国', '第一滴血', '指环王', '霍比特人', '速度与激情', '指环王']

print('------删除之前------')
for tempName in movieName:
    print(tempName)

movieName.remove('指环王')

print('------删除之后------')
for tempName in movieName:
    print(tempName)

#列表去重
ids = [1,2,3,3,4,2,3,4,5,6,1]
news_ids = []
for id in ids:
    if id not in news_ids:
        news_ids.append(id)
print (news_ids)


class X(object):
    def __init__(self, a, b, range):
        self.a = a
        self.b = b
        self.range = range
    def __call__(self, a, b):
        self.a = a
        self.b = b
        print('__call__ with （{}, {}）'.format(self.a, self.b))
    def __del__(self, a, b, range):
        del self.a
        del self.b
        del self.range
xInstance = X(1, 2, 3)
xInstance(1,2)



for i in range(5):
    print(i)