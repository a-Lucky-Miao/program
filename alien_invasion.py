import sys
from random import randint
from time import sleep
import pygame
from setting import Setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Aline
from star import Star


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏"""
        # 初始化模块
        pygame.init()
        self.settings = Setting()
        # 创建一个surface对象窗口
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(" Alien Invasion")
        """创建所需信息"""
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.stars = pygame.sprite.Group()
        self.create_stars(self.settings.screen_width,
                          self.settings.screen_height,
                          self.settings.max_x_space, self.settings.max_y_space)
        # 创建按钮
        self.play_button = Button(self, "play")

    def run_game(self):
        """运行游戏"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_screen(self):
        """屏幕更新"""
        # 每次循环时都重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        # 绘画星星背景
        self.stars.draw(self.screen)
        # 绘画飞船
        self.ship.blitme()
        # 绘画子弹
        for bullet in self.bullets.sprites():
            """更新屏幕上的图像,并切换到新屏幕"""
            bullet.draw_bullet()
        # 绘画外星人
        self.aliens.draw(self.screen)
        # 显示游戏分数
        self.sb.show_score()
        # 如果处于非游戏就绘制Play
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _check_events(self):
        """响应键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下按钮事件
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 抬起按钮事件
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # 鼠标监听
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """按下按钮事件"""
        # 按上键飞船向上设为Ture
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        # 按下键飞船向下设为Ture
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        # 按空格发射子弹
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # 按Q键退出游戏
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """抬起按钮事件"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一个子弹并将其加入编组的bullet中"""
        # 小于最大子弹数创建子弹
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            # 将子弹加入到子弹数组中
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置并删除消失子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除消失子弹
        for bullet in self.bullets.copy():
            # 右部碰撞
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        # 检测子弹碰撞外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """检测子弹碰撞外星人"""
        collections = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                 True, True)
        # 碰撞得分
        if collections:
            for aliens in collections.values():
                # 分数增加
                self.stats.score += self.settings.alien_points
                # 显示分数
                self.sb.prep_score()
                # 检查是否高于最高分
                self.sb.check_high_score()
        # 消灭外星人
        if not self.aliens:
            self.bullets.empty()
            # 创建外星人群
            self._create_fleet()
            # 增加游戏速度
            self.settings.increase_speed()
            # 等级增加
            self.stats.level += 1
            # 显示等级
            self.sb.prep_level()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人
        alien = Aline(self)
        alien_width, alien_height = alien.rect.size
        # 定义外星人群行与列
        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_aliens_y = available_space_y // (2 * alien_height)
        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_width - (3 * alien_width) +
                             ship_width)
        number_rows = available_space_x // (2 * alien_width)

        # 创建一组外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_y):
                self._create_aline(alien_number, row_number)

    def _create_aline(self, alien_number, row_number):
        """创建一个外星人并将其加入当前行"""
        alien = Aline(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + 2 * alien_height * alien_number
        alien.rect.y = alien.y
        alien.rect.x = self.settings.screen_width - 2 * alien_width * row_number
        # 将外星人并将其加入当前外星人列
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人群中所有外星人位置"""
        # 检测外星人是否左右碰撞
        self._check_fleet_edges()
        # 外星人更新
        self.aliens.update()
        # 判断外星人是否与飞船碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 判断外星人是否下边框碰撞
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """检测外星人是否碰撞边缘"""
        for aline in self.aliens.sprites():
            if aline.check_edges():
                self._change_fleet_direction()
                break

    def create_star(self, star_right_coordinate, random_x_space,
                    star_bottom_coordinate, random_y_space):
        # 创建一个星星
        star = Star(self)
        # 新增星星左坐标为前一个星星右坐标加随机横间距
        star.rect.x = star_right_coordinate + random_x_space
        # 每行星星上方留出适当空间
        star.rect.y = star_bottom_coordinate + random_y_space
        # 将星星增添到星星群
        self.stars.add(star)

    def create_stars(self, screen_width, screen_height, max_x_space,
                     max_y_space):
        star = Star(self)
        # 记录前一个星星右坐标
        star_right_coordinate = 0
        # 记录前行星星底坐标
        star_bottom_coordinate = 0
        # 增加随机列间距
        random_x_space = randint(1, max_x_space)
        # 增加随机行间距
        random_y_space = randint(1, max_y_space)
        # 屏幕纵向空间足够时循环创建整行星星
        while star_bottom_coordinate + star.rect.height + random_y_space < screen_height:
            # 屏幕横向空间足够时循环创建单个星星
            while star_right_coordinate + star.rect.width + random_x_space < screen_width:
                self.create_star(star_right_coordinate, random_x_space,
                                 star_bottom_coordinate, random_y_space)
                # 重置前一个星星右坐标和随机横间距
                star_right_coordinate = star_right_coordinate + star.rect.width + random_x_space
                random_x_space = randint(1, max_x_space)
            # 重置前一个星星右坐标、前行星星底坐标和随机纵间距
            star_right_coordinate = 0
            star_bottom_coordinate = star_bottom_coordinate + star.rect.height + random_y_space
            random_y_space = randint(1, max_y_space)

    def _change_fleet_direction(self):
        """碰撞改变移动方向"""
        for aline in self.aliens.sprites():
            aline.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_play_button(self, mouse_pos):
        """点击按钮"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            # 新的开局
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            # 鼠标不显示
            pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """"判断外星人是否与飞船碰撞"""
        # 生命条还存在
        if self.stats.ships_left > 0:
            # 生命条减少
            self.stats.ships_left -= 1
            # 新的开局
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            # 游戏结束
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """判断外星人是否下边框碰撞"""
        for aline in self.aliens.sprites():
            if aline.rect.left < 0:
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏实列并运行
    ai = AlienInvasion()
    ai.run_game()
