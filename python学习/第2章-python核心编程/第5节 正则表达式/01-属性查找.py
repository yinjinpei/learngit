# coding:utf-8
# author:YJ沛


class test():
    test_1 = 100

    def __init__(self):
        self.test_2 = 200

    def test3(self):
        print("test3")

t1 = test()
# 查看这个t1对象的所有属性，列表方式保存
for i in t1.__dir__():
    print(i)

print("---------------------------------")

# 查看这个t1对象的所有属性的 键和值，字典方式保存
print(t1.__dict__)