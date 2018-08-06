
class Test(object):
    def __init__(self,switch):
        self.switch = switch    #捕获异常开关

    def calc(self,a,b):
        try:
            return a/b

        except Exception as result:
            if self.switch:
                print("开启捕获，并已经捕获到了异常，信息如下：")
                print(result)
            else:
                #重新抛出这个异常，此时就会被这个异常处理给捕获到，从而触发默认的异常处理
                raise


def main():
    # 捕获异常开关
    abnormal_switch = input("开启捕获异常模式请输入:True ，否则输入:False\t:")
    dividend = int(input("请输入 被除数 数字："))
    divisor = int(input("请输入 除数 数字："))

    test=Test(abnormal_switch)  #被除数
    test.calc(dividend,divisor) #除数


main()
