class GameStats:

    def __init__(self, ai_game):
        """游戏得分以及最高分"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        # 读取最高分
        with open('program/high_score.txt', 'r') as high_score:
            highscore = high_score.read()
        # 如果为空则设为0
        if highscore == "":
            self.high_score = 0
        else:
            self.high_score = int(highscore)
        self.level = 1

    def reset_stats(self):
        """初始化得分"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
