#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11 21:24
# @Author  : HU
# @File    : settings.py
# @Software: PyCharm Community Edition


class Settings:
    """存储《外星人入侵》的所以设置"""

    def __init__(self):
        """
        初始化游戏设置
        游戏静态设置
        """
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        # 数量上限
        self.ships_limit = 3

        # 子弹设置
        # 外形
        self.bullet_width = 4
        self.bullet_height = 8
        self.bullet_color = (60, 60, 60)
        # 数量
        self.bullets_allowed = 10

        # 外星人是在
        # 行数、列数上限
        self.alien_number_max_rows = 2
        self.alien_number_max_cols = 5

        # 按钮设置
        # 文字提示
        self.button_msg = ['Play', 'Pause']

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 分值提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        初始化随游戏进行而变化的设置
        游戏动态设置
        """
        # 飞船
        self.ship_speed_factor = 0.5
        # 子弹
        self.bullet_speed_factor = 2
        # 外星人
        self.alien_speed_factor = 0.2
        self.fleet_drop_speed = 2

        # fleet_direction 为1向右，为-1向左
        self.fleet_direction = 1

        # 外星人分值
        self.alien_points = 50

    def increase_speed(self):
        """
        加快游戏节奏
        提高速度设置
        """
        # 提高速度
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        # 提高分值
        self.alien_points = int(self.alien_points * self.score_scale)
