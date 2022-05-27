import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 加载外星人图像并设置其rect属性
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('program/images/ship.bmp')
        # 向右旋转90
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        self.center_ship()

        # 移动标识
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船而不是修改y值
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.ship_spead
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_spead
        # 根据self.y跟新rect对象
        self.rect.y = self.y

    def blitme(self):
        """"在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """"在指定绘制飞船位置"""
        # 每个飞船初始在屏幕左方中间
        self.rect.midleft = self.screen_rect.midleft
        # 在飞船的属性y中储存最小y值
        self.y = float(self.rect.y)
