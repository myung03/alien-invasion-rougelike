import sys 
from time import sleep

import pygame

from stats.settings import Settings
from stats.game_stats import GameStats
from stats.scoreboard import Scoreboard
from sprites.ship import Ship
from sprites.alien import Alien 
from sprites.bullet import Bullet
from sprites.star import Star
from sprites.button import Button

from random import randint 

class AlienInvasion:
    """Master class"""
    def __init__(self):
        """Init game"""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)

        #screen settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.bg_color = (0, 0, 0) 
        self.star = pygame.image.load('images/star_0.png')
        pygame.display.set_caption("Alien Invasion")

        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        #load background + fleet 
        self._create_fleet()
        self._draw_stars()

        #load playbutton 
        self.play_button = Button(self, "Start")

      
    
    def _check_events(self):
        """Handle key and mouse events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
        
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)
                
                                   
    def _check_keydown_events(self, event):
      """Handles keydown events"""
      if event.key == pygame.K_RIGHT:
            self.ship.keys['right'] = True
      if event.key == pygame.K_LEFT:
             self.ship.keys['left'] = True
      if event.key == pygame.K_UP:
            self.ship.keys['up'] = True
      if event.key == pygame.K_DOWN:
            self.ship.keys['down'] = True
      if event.key == pygame.K_q:
           sys.exit() 
      if event.key == pygame.K_SPACE:
           self._fire_bullet()
    
    def _check_keyup_events(self, event):
      if event.key == pygame.K_RIGHT:
            self.ship.keys['right'] = False
      if event.key == pygame.K_LEFT:
             self.ship.keys['left'] = False
      if event.key == pygame.K_UP:
            self.ship.keys['up'] = False
      if event.key == pygame.K_DOWN:
            self.ship.keys['down'] = False

    def _check_play_button(self, mouse_pos):
         """Start game when start is pressed"""
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.stats.game_active:
              #Reset game 
              self.settings.initialize_dynamic_settings()
              self.stats.reset_stats()
              self.stats.game_active = True
              self.aliens.empty()
              self.bullets.empty()
              self.sb.prep_score()
              self.sb.prep_level()
              self.sb.prep_ships()
              pygame.mouse.set_visible(False)


              #Create new fleet
              self._create_fleet()

    def _fire_bullet(self):
        """Create new bullet on screen"""
        if len(self.bullets) < self.settings.max_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _create_fleet(self):
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size

         #max width/height of rows/cols
         available_space_x = self.settings.screen_width - (35 * alien_width)
         number_aliens_x = available_space_x // (4 * alien_width)

         ship_height = self.ship.rect.height
         available_space_y = (self.settings.screen_height // 10
                              - (3 * alien_height) - ship_height)
         number_rows = available_space_y // (2 * alien_height) 

         for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): 
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, a_number, r_number):
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         alien_width = alien.rect.width 
         alien.x = alien_width + 3 * alien_width * a_number
         alien.rect.x = alien.x
         alien.rect.y = (alien.rect.height + 4 * alien.rect.height * r_number) + 100
         self.aliens.add(alien)
    
    def _check_fleet_edges(self):
         """Go through fleet and see if sides have reached ends """
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_dir()
                   break
    
    def _change_fleet_dir(self):
         """Drop fleet and change direction"""
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= - 1
        
    def _update_aliens(self):
         """Update all aliens in fleet"""
         self._check_fleet_edges()
         self.aliens.update()

         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._check_ship_hit()
        
         self._check_aliens_bottom()

    def _update_bullets(self):
         self.bullets.update()
         """Remove bullets off screen"""
         for bullet in self.bullets.copy():
              if bullet.rect.bottom <= 0:
                   self.bullets.remove(bullet)

         self._check_collisions()

    
    def _check_collisions(self):
         """Check for collisions and spawn next waves"""
         collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

         if collisions:
                 for aliens in collisions.values():
                       self.stats.score += self.settings.aliens_points * len(aliens)
                 self.sb.prep_score()
                 self.sb.check_high_score()

         if not self.aliens: 
              self.bullets.empty()
              self._create_fleet()
              self.settings.increase_speed()

              #increase level
              self.stats.level += 1
              self.sb.prep_level()
    
    def _check_ship_hit(self):
         """Remove a life if ship hit"""
         if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            """Remove all aliens and bullets, and then pause game briefly"""
            self.aliens.empty()
            self.bullets.empty()
            sleep(0.5)
         else: 
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

         self._create_fleet()

    def _check_aliens_bottom(self):
         """Check if aliens hit bottom"""
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   self._check_ship_hit
                   break

    def _draw_stars(self):
         for x in range(750):
              star = Star(self)
              star.x = randint(20, self.settings.screen_width - 20)
              star.y = randint(20, self.settings.screen_height - 20)
              star.rect.x = star.x
              star.rect.y = star.y 
              self.stars.add(star)
              
        
        
    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
             bullet.blitme()
        
        self.aliens.draw(self.screen)

        #Update score info
        self.sb.show_score()

        #draw play button if inactive 
        if not self.stats.game_active:
             self.play_button.draw_button()

        #makes the most recently drawn screen visible 
        pygame.display.flip()
                
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            

        
                   
    

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()