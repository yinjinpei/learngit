
class Msg:

    #私有方法
    def __sendMsg(self):
        print("正在发送短信......")

    #公有方法
    def getMsg(self,money):
        if money > 10000:
            self.__sendMsg()    #在类内可以调 用
        else:
            print("余额不足，请充值！！！")



tom = Msg()
tom.getMsg(100) #for test
tom.getMsg(100000)
#tom.__sendMsg() #私有方法直接调用不了
