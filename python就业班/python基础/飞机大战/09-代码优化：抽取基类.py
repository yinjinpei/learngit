# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time
import random

#飞机基类
class BasePlane(object):
    def __init__(self,screen_temp,x,y,image_name):
        self.screen = screen_temp
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_name)
        self.bullet_list = []   #存储发射出去的子弹对象引用

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():  #判断子弹是否越界
                self.bullet_list.remove(bullet)

#创建飞机
class HeroPlane(BasePlane):

    def __init__(self,screen_temp):
        super().__init__(screen_temp,210,700,"./feiji/hero1.png")

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10

    def fire(self): #发射子弹
        self.bullet_list.append(Bullet(self.screen,self.x,self.y))


class EnemyPlane(BasePlane):
    def __init__(self,screen_temp):
        super().__init__(screen_temp,0,0,"./feiji/enemy0.png")
        self.direction = "right"    #用来存储敌人飞机默认的移动方向


    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5

        if self.x >=430:
            self.direction = "left"
        elif self.x <=0:
            self.direction = "right"

    def fire(self):
        random_num = random.randint(1,60)
        if random_num == 1 or random_num == 50:
            self.bullet_list.append(EnemyBullet(self.screen,self.x,self.y))


#子弹基类
class BaseBullet(object):
    def __init__(self, screen_temp,x,y,image_name):
        self.screen = screen_temp
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


#创建子弹
class Bullet(BaseBullet):
    def __init__(self,screen_temp,x,y):
        super().__init__(screen_temp,x+30,y-20,"./feiji/bullet.png")

    def move(self):
        self.y -= 15

    def judge(self):
        #if self.y < 200:   for test #子弹越界位置
        if self.y < 0:
            return True
        else:
            return False

#创建敌人飞机子弹
class EnemyBullet(BaseBullet):
    def __init__(self,screen_temp,x,y):
        super().__init__(screen_temp,x+25,y+30,"./feiji/bullet1.png")


    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False


############ 添加按键功能 #########
def key_control(hero_temp):
    for event in pygame.event.get():

        # 判断是否是点击了退出按键
        if event.type == QUIT:
            print("exit")
            exit()

        # 判断是否是按下了按键
        elif event.type == KEYDOWN:

            # 判断是否是点击了a或者left
            if event.key == K_a or event.key == K_LEFT:
                hero_temp.move_left()
                print(("left"))

            # 判断是否是点击了d或者right
            if event.key == K_d or event.key == K_RIGHT:
                hero_temp.move_right()
                print(("right"))

            # 判断是否是点击了空格键
            if event.key == K_SPACE:
                print("space")
                hero_temp.fire()



def main():
    '''控制程序流程'''

    #1,创建一个显示主窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2,创建背景图片
    background = pygame.image.load("./feiji/background.png")

    #3,创建一架飞机图片
    hero = HeroPlane(screen)

    #4,创建敌人飞机
    enemy = EnemyPlane(screen)

    while True:

        screen.blit(background,(0,0))   #把背景图片显示到主窗口中
        hero.display()          #把飞机图片显示到主窗口中
        enemy.display()         #把敌人飞机图片显示到主窗口中
        enemy.move()
        enemy.fire()            #敌人飞机开火
        pygame.display.update() #显示画面
        key_control(hero)       #添加按键功能
        time.sleep(0.01)        #睡眠，主要降低CPU使用率


if __name__ == "__main__":
    main()





