#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/12 8:43
# @Author  : HU
# @File    : game_functions.py
# @Software: PyCharm Community Edition


import sys
from time import sleep

import pygame
# from random import randint

from button import Button
from bullet import Bullet
from alien import Alien


def check_keydown_event(event, ai_settings, screen, stats,
                        ship, aliens, bullets, sb):
    """响应按键"""
    # 上、下、左、右移动，及发射子弹
    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # 按P键快速开始游戏
    elif event.key == pygame.K_p and \
            not stats.game_active and \
            not stats.game_pause:
        start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)
    # 按Q键退出
    elif event.key == pygame.K_q:
        sys.exit()
    # 按ESC暂停（bug:按ESC也能开始游戏！）
    elif event.key == pygame.K_ESCAPE:
        if stats.game_active:
            stats.game_active = False
            stats.game_pause = True
        else:
            stats.game_active = True
            stats.game_pause = False


def check_keyup_event(event, ship):
    """响应松开"""
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def start_game(ai_settings, screen, stats, ship, aliens, bullets, sb):
    """开始游戏"""
    # （重置游戏设置）
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图像
    sb.prep_score()
    # sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def create_button(ai_settings, screen):
    """创建按钮列表"""
    button_lists = []
    for msg in ai_settings.button_msg:
        button = Button(ai_settings, screen, msg)
        button_lists.append(button)
    return button_lists


def check_play_button(ai_settings, screen, stats,
                      ship, aliens, bullets, play_button, sb, mouse_x, mouse_y):
    """单击Play开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.game_pause:
        # 开始游戏（重置游戏）
        start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)


def check_events(ai_settings, screen, stats,
                 ship, aliens, bullets, play_button, sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, stats,
                                ship, aliens, bullets, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,
                              ship, aliens, bullets, play_button, sb,
                              mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats,
                  ship, aliens, bullets, play_button, pause_button, sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 在指定位置绘制飞船
    ship.blitme()
    # 在指定位置绘制外星人
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活跃状态且不在暂停状态就绘制Play按钮
    # 如果如果游戏处于非活跃状态且在暂停状态就绘制Pause按钮
    if not stats.game_active:
        if not stats.game_pause:
            play_button.draw_button()
        elif stats.game_pause:
            pause_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats,
                   ship, aliens, bullets, sb):
    # 更新子弹位置
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检测撞击，做出响应
    check_bullet_alien_collision(ai_settings, screen, stats,
                                 ship, aliens, bullets, sb)


def check_bullet_alien_collision(ai_settings, screen, stats,
                                 ship, aliens, bullets, sb):
    # 检查是否有子弹击中了外星人
    # 如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            # 实时记录，转换为图片
            sb.prep_score()
        # 检查最高分是否被打破，并作出响应
        check_high_score(stats, sb)

    # 检测外星人剩余个数，做出相应对策
    if len(aliens) == 0:
        # 如果整群外星人被消灭了
        # 删除现有子弹，并新建一群外星人，加快游戏节奏
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到限制就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    # 并计算一行可容纳几个外星人,外星人间距为外星人宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建多行外形人，行数和列数不超过默认最大设置
    for row_number in range(
            min(number_rows, ai_settings.alien_number_max_rows)):
        # for alien_number in range(randint(1, number_aliens_x)):
        for alien_number in range(
                min(number_aliens_x, ai_settings.alien_number_max_cols)):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边界时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            chang_fleet_direction(ai_settings, aliens)
            break


def chang_fleet_direction(ai_settings, aliens):
    """将整个外星群下移，并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, ship, sb):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        ship.center_ship()

        # 更新记分牌
        sb.prep_ships()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def aliens_screen_bottom(ai_settings, stats, screen,
                         ship, aliens, bullets, sb):
    """外星人到达屏幕底端"""
    if stats.ships_left > 0:
        # ships_left 减1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新外星人，并将外星人放在屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 更新记分牌
        sb.prep_ships()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 作出响应
            aliens_screen_bottom(ai_settings, stats, screen,
                                 ship, aliens, bullets, sb)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """
    检查是否有外星人位于屏幕边缘
    并更新外星人群位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人与飞船之间的碰撞
    aliens_hit = pygame.sprite.spritecollide(ship, aliens, True)
    if len(aliens_hit) > 0:
        ship_hit(stats, ship, sb)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
