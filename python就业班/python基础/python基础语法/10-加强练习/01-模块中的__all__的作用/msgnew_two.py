__all__ = ["test1","test2","number","Test3"]    #只有在这里定义了下面的函数，类等内容才能被调用


def test1():
    print("------msgnew_two.test1------")

def test2():
    num = 100
    return num

class Test3(object):
    def test_print(self):
        print("----msgnew_two.Test3.test_print----")

number = 10000