#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 9:48
# @Author  : HU
# @File    : scoreboard.py
# @Software: PyCharm Community Edition


import pygame.font
from pygame.sprite import Group

from ship import Ship


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化得分属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分时字体设置
        self.text_color = (60, 60, 60)
        self.text_size = 24
        self.font = pygame.font.SysFont(None, self.text_size)

        # 设置边距
        self.bound_distance = 10

        # 显示当前得分图像
        self.prep_score()
        # 显示最高得分图像
        self.prep_high_score()
        # 显示等级图像
        self.prep_level()
        # 显示剩余飞船数量
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color)

        # 放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = \
            self.screen_rect.right - self.text_size
        self.score_rect.top = \
            self.screen_rect.top + self.text_size / 2

    def prep_high_score(self):
        """将最高分转换为图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "BEST: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = \
            self.screen_rect.centerx
        self.high_score_rect.top = \
            self.screen_rect.top + self.text_size / 2

    def prep_level(self):
        """将等级转换为图像"""
        self.level_image = self.font.render(
            "Level: " + str(self.stats.level), True, self.text_color,
            self.ai_settings.bg_color)

        # 放在屏幕顶部中央
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = \
            self.screen_rect.right - self.text_size
        self.level_rect.top = \
            self.score_rect.bottom + self.text_size / 2

    def prep_ships(self):
        """显示剩余飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = self.bound_distance + ship_number * ship.rect.width
            ship.rect.y = self.bound_distance
            self.ships.add(ship)

    def show_score(self):
        """屏幕显示"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
