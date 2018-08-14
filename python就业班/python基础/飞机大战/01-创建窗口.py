# -*- coding:utf-8 -*-
import pygame
import time

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
        screen.blit(hero,(200,700))

        #显示画面
        pygame.display.update()


        #睡眠，主要降低CPU使用率
        time.sleep(0.01)



if __name__ == "__main__":
    main()





