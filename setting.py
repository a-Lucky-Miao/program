class Setting:
    """储存游戏外星人入侵中的所有设置类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_spead = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 3
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        # 允许最大子弹数
        self.bullets_allowed = 3

        # 外星人
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction 1表示向右 -1表示向左
        self.fleet_direction = 1
        # 击杀得分
        self.alien_points = 50

        # 速度倍数
        self.speedup_scale = 1.1
        # 击杀分数倍数
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # 设置星星间距最大值
        self.max_x_space = 100
        self.max_y_space = 100

    def initialize_dynamic_settings(self):
        """各个速度初始值"""
        self.ship_spead = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        # fleet_direction 1表示向右 -1表示向左
        self.fleet_direction = 1
        # 击杀得分
        self.alien_points = 50

    def increase_speed(self):
        """各个初始值翻倍"""
        self.ship_spead *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= int(self.alien_points * self.score_scale)
