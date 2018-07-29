class Game(object):
    #类属性
    num = 0

    #实例方法
    def __init__(self):
        #实例属性
        self.name = "peter"
        #Game.num += 1   #第1种，通过类名修改类属性
        #print(Game.num)

    #类方法
    @classmethod
    def add_num(cls):
        cls.num += 1   #第2种，通过类方法修改类属性
        print(cls.num)

    #静态方法，一般用于和对象、类无关
    @staticmethod
    def print_game_name(new_game_name):
        name = new_game_name
        print("-------------------")
        print("  "+name)

    # 静态方法，一般用于和对象、类无关
    @staticmethod
    def print_game():
        print("  1,开始游戏")
        print("  2,结束游戏")
        print("-------------------")

game=Game()
game.add_num()
#第1种调用方法
Game.print_game_name("王者荣耀")
Game.print_game()
print("")
#第2种调用方法
Game.print_game_name("英雄联盟")
Game.print_game()




