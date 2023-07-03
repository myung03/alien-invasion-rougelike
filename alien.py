import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):

    def __init__(self, ai_game):
        """Create an alien"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/enemy_0.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #exact decimal point location 
        self.x = float(self.rect.x)
    
    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        """Return boolean value checking whether alien at edge of screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    

