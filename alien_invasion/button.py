#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 13:46
# @Author  : HU
# @File    : button.py
# @Software: PyCharm Community Edition


import pygame.font


class Button:

    def __init__(self, ai_settings, screen, msg):
        """初始化按钮"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 100, 50
        self.button_coler = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg渲染为图像"""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_coler)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮"""
        self.screen.fill(self.button_coler, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
