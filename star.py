import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """管理星星类"""

    def __init__(self, ai_game):
        """初始化星星"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('program/images/star.jpg')
        self.rect = self.image.get_rect()
