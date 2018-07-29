class Game(object):
    #类属性
    num = 0

    def __init__(self,new_name):
        self.name = new_name
        Game.num += 1   #通过类名修改类属性


game=Game("王者荣耀")
print(game.num)     #第1种，通过对象调用类属性
print(Game.num)     #第2种，通过类名调用类属性

