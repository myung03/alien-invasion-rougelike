import pygame
from pygame.sprite import Sprite 

class Star(Sprite):

    def __init__(self, ai_game):
        """Create an alien"""
        super().__init__()
        self.screen = ai_game.screen

        self.image = pygame.image.load('images/star_1.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #exact decimal point location 
        self.x = float(self.rect.x)