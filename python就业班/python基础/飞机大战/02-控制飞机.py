# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import time

k_x = 210
k_y = 700

def main():
    '''控制程序流程'''

    #1,创建一个显示主窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2,创建背景图片
    background = pygame.image.load("./feiji/background.png")

    #3,创建一架飞机图片
    hero = pygame.image.load("./feiji/hero1.png")

    while True:
        #把背景图片显示到主窗口中
        screen.blit(background,(0,0))

        #把飞机图片显示到主窗口中
        screen.blit(hero,(k_x,k_y))

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
                if event.type == K_a or event.type == K_LEFT:
                    k_x = k_x + 1
                    print(("left"))

                # 判断是否是点击了d或者right
                if event.type == K_d or event.type == K_RIGHT:
                    k_x = k_x - 1
                    print(("right"))

                # 判断是否是点击了空格键
                if event.type == K_SPACE:
                    print("space")


        #睡眠，主要降低CPU使用率
        time.sleep(0.01)



if __name__ == "__main__":
    main()





