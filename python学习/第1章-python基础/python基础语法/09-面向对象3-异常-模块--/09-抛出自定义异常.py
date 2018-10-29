class ShortInputExecption(Exception):
    '''自定义的异常类'''
    def __init__(self,length,atleast):
        self.length = length
        self.atleast = atleast


def main():
    try:
        num = input("输入数字:  ")
        if len(num) < 5:
            raise ShortInputExecption(len(num),5)

    except ShortInputExecption as result:
        print("StopAsyncIteration：输入的长度为：%d，长度至少应为：%d"%(result.length,result.atleast))

    else:
        print("没有发生异常。。。")

main()