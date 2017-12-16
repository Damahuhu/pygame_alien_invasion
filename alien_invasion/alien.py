#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/12 19:25
# @Author  : HU
# @File    : alien.py
# @Software: PyCharm Community Edition


import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """初始化外星人，并设置其位置"""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人人图像，设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人准确位置
        self.x = float(self.rect.x)
        # self.y = float(self.rect.y)

    def blitem(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """
        向左或右移动外星人
        向下移动外星人？
        """
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        # self.y += self.ai_settings.fleet_drop_speed
        # self.rect.y = self.y
