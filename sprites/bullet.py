import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Manages a ship's bullets"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        

        #Create bullet, set to correct position 

        self.image = pygame.image.load('images/pbullet.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        #pos of bullet 
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up on screen"""
        self.y -= self.settings.bullet_speed

        #Update bullet rect pos
        self.rect.y = self.y
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
