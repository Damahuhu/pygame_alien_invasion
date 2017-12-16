#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 12:22
# @Author  : HU
# @File    : game_stats.py
# @Software: PyCharm Community Edition


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 游戏刚启动时处于非活跃状态
        self.game_active = False
        # 暂停状态标志
        self.game_pause = False

        # 在任何情况下都不应重置最高分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        # 飞船剩余数量
        self.ships_left = self.ai_settings.ships_limit

        # 玩家得分数
        self.score = 0

        # 玩家等级
        self.level = 1
