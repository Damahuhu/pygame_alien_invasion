#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/11 20:58
# @Author  : HU
# @File    : alien_invasion.py
# @Software: PyCharm Community Edition


import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
# from button import Button
from ship import Ship
# from alien import Alien
import game_functions as gf


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建所以按钮
    button_lists = gf.create_button(ai_settings, screen)
    # 创建Play按钮
    play_button = button_lists[0]
    # 创建Pause按钮
    pause_button = button_lists[1]

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个用于存储外星人的编组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats,
                        ship, aliens, bullets, play_button, sb)

        if stats.game_active and not stats.game_pause:
            # 更新飞船位置
            ship.update()
            # 更新子弹位置,（数量）;以及检测撞击事件，删除相应的子弹和飞船
            gf.update_bullets(ai_settings, screen, stats,
                              ship, aliens, bullets, sb)
            # 更新外星人位置
            gf.update_aliens(ai_settings, stats, screen,
                             ship, aliens, bullets, sb)

        # 更新屏幕上的图像，并切换到新屏幕
        gf.update_screen(ai_settings, screen, stats,
                         ship, aliens, bullets, play_button, pause_button, sb)


run_game()
