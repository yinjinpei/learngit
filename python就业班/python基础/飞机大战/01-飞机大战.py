# -*- coding:utf-8 -*-
import pygame
import time

def main():
    #1，创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((480,652),0,32)

    #2,创建一个和窗口一样大的图片，用来当背景
    background = pygame.image.load("./feiji/background.png")

    while True:
        #设定需要显示的背景图
        screen.blit(background,(0,0))

        #更新需要显示的内容
        pygame.display.update()

        time.sleep(0.01)



if __name__ == "__main__":
    main()