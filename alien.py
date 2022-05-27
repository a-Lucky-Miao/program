import pygame
from pygame.sprite import Sprite


class Aline(Sprite):
    """表示单个外星人类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('program/images/alien.bmp')
        self.rect = self.image.get_rect()
        # 每个外星人初始在屏幕右下角附近
        self.rect.x = 1400
        self.rect.y = 800

        # 储存外星人精准的垂直位置
        self.y = float(self.rect.y)

    def update(self):
        """上下移动"""
        self.y -= (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.y = self.y

    def check_edges(self):
        """如果外星人位于屏幕边缘就返回true"""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.y <= 0:
            return True
