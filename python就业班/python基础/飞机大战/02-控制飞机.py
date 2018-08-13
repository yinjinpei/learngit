# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time



def main():
    '''控制程序流程'''

    #1,创建一个显示主窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2,创建背景图片
    background = pygame.image.load("./feiji/background.png")

    #3,创建一架飞机图片
    hero = pygame.image.load("./feiji/hero1.png")

    x = 210
    y = 700

    while True:
        #把背景图片显示到主窗口中
        screen.blit(background,(0,0))

        #把飞机图片显示到主窗口中
        screen.blit(hero,(x,y))

        #显示画面
        pygame.display.update()

        ############ 添加按键功能 #########
        for event in pygame.event.get():

            #判断是否是点击了退出按键
            if event.type == QUIT:
                print("exit")
                exit()

            #判断是否是按下了按键
            elif event.type == KEYDOWN:

                #判断是否是点击了a或者left
                if event.key == K_a or event.key == K_LEFT:
                    x -= 5
                    print(("left"))

                # 判断是否是点击了d或者right
                if event.key == K_d or event.key == K_RIGHT:
                    x += 5
                    print(("right"))

                # 判断是否是点击了空格键
                if event.key == K_SPACE:
                    print("space")


        #睡眠，主要降低CPU使用率
        time.sleep(0.01)



if __name__ == "__main__":
    main()





