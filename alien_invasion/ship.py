#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11 21:53
# @Author  : HU
# @File    : ship.py
# @Software: PyCharm Community Edition


import pygame
from  pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩阵
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数
        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # 移动标志
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船的center值，而不是
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        if self.moving_right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left:
            self.centerx -= self.ai_settings.ship_speed_factor
        # 到达边缘，就从另一边出现(上、下不可以)
        if self.moving_right and self.rect.right >= self.screen_rect.right:
            self.centerx = self.screen_rect.left
        if self.moving_left and self.rect.left <= self.screen_rect.left:
            self.centerx = self.screen_rect.right

        # 根据center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.centerx = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
