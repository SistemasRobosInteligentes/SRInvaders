import pygame
from random import uniform

class Ammobox(pygame.sprite.Sprite):
    def __init__(self, y_position, screen_width,camera_height,screen_height, player_user):
        super().__init__()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_user = player_user
        self.y_position = y_position
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.image = pygame.transform.scale(pygame.image.load('Images/quiver.png').convert_alpha(),(round(40*self.screen_width/1920),round(40*self.screen_width/1920)))
        else:
            self.image = pygame.transform.scale(pygame.image.load('Images/quiver.png').convert_alpha(),(round(40*self.screen_height/1080),round(40*self.screen_height/1080)))

            
            
        
        if self.player_user.x_pos < self.screen_width/2:
            x = self.screen_width/2 + self.screen_width*uniform(0.2,0.45)
        else:
            x = self.screen_width/2 - self.screen_width*uniform(0.15,0.40)
            
            
            
        self.rect = self.image.get_rect(midbottom = (x,self.y_position)) #

    def update(self):
        self.rect.x += 0

        