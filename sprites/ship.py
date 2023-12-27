import pygame 
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        """init ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/ship.png')

        #ship graphical/settings
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

         #Movement bools and values 
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.keys = {'right': False, 
                     'left': False, 
                     'down': False, 
                     'up': False, }

    
    def update(self):
        """Update the ship's location based on move flag"""
        if self.keys['right'] and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.keys["left"] and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.keys["down"] and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed 
        if self.keys["up"] and self.rect.top > self.screen_rect.height / 1.5:
            self.y -= self.settings.ship_speed
        
        self.rect.x = self.x
        self.rect.y = self.y
            
    def blitme(self):
        self.screen.blit(self.image, self.rect)
