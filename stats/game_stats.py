class GameStats:
    """Track stats for a save file of Alien Invasion"""
    def __init__(self, ai_game):
        """init stats"""
        self.settings = ai_game.settings

        self.high_score = 0
        self.level = 1

        self.reset_stats()
        self.game_active = False

    
    def reset_stats(self):
        """Variable stats"""
        self.ships_left = self.settings.ship_limit
        self.score = 0 