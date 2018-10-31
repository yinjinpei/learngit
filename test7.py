
class A(object):
    def __init__(self):
        self.abc = 123


class B(object):
    # def __init__(self):
    #     self.abc = 222
    pass

class C(A):
    def __init__(self):
        self.abc =333

class D(B,C):
    pass



d = D()
print(d.abc)