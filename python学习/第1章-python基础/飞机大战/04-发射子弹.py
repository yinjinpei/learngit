# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time


class HeroPlane(object):

    def __init__(self,screen_temp):
        self.image = pygame.image.load("./feiji/hero1.png")
        self.x = 210
        self.y = 700
        self.screen = screen_temp
        self.bullet_list = []   #存储发射出去的子弹对象引用

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()

    def move_left(self):
        self.x -= 10

    def move_right(self):
        self.x += 10

    def fire(self):
        self.bullet_list.append(Bullet(self.screen,self.x,self.y))


#创建子弹
class Bullet(object):
    def __init__(self,screen_temp,x,y):
        self.image = pygame.image.load("./feiji/bullet.png")
        self.x = x+40
        self.y = y-20
        self.screen = screen_temp

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 5


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


    while True:

        screen.blit(background,(0,0))   #把背景图片显示到主窗口中
        hero.display()          #把飞机图片显示到主窗口中
        pygame.display.update() #显示画面
        key_control(hero)       #添加按键功能
        time.sleep(0.01)        #睡眠，主要降低CPU使用率


if __name__ == "__main__":
    main()





