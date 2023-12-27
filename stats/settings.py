class Settings:

    def __init__(self):
        """init game settings"""

        #SCREEN
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        #SHIP
        self.ship_speed = 2.0
        self.ship_limit = 3

        #BULLETS
        self.bullet_speed = 10.0
        self.max_bullets = 5

        #ALIENS 
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.aliens_points = 50

        #GAME SCALE ON LEVEL
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Init settings that change throughout game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet direction of 1 is right, -1 is left
        self.fleet_direction = 1.0

        
    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.aliens_points = int(self.aliens_points * self.score_scale)