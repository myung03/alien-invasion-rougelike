class Settings:

    def __init__(self):
        """init game settings"""

        #SCREEN
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        #SHIP
        self.ship_speed = 3
        self.ship_limit = 3

        #BULLETS
        self.bullet_speed = 10.0
        self.max_bullets = 5

        #ALIENS 
        self.alien_speed = 3.0
        self.fleet_drop_speed = 1
        self.fleet_direction = 1
