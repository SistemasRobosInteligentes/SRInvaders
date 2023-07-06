import pygame
from random import randint

class Powerups(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screen_height, screen_width):
        super().__init__()
        self.random_value = randint(0,2)
        self.screen_height = screen_height
        self.screen_width = screen_width
        
        if(self.random_value == 0):
            self.name = "plus_1_life"
            if (self.screen_width/1920 < self.screen_height/1080):
                self.image = pygame.transform.scale(pygame.image.load("Images/golden_apple.png").convert_alpha(),(round(40*self.screen_width/1920),round(40*self.screen_width/1920)))
            else:
                self.image = pygame.transform.scale(pygame.image.load("Images/golden_apple.png").convert_alpha(),(round(40*self.screen_height/1080),round(40*self.screen_height/1080)))
        elif(self.random_value == 1):
            self.name = "plus_1_arrow"
            if (self.screen_width/1920 < self.screen_height/1080):
                self.image = pygame.transform.scale(pygame.image.load("Images/strength_potion.png").convert_alpha(),(round(40*self.screen_width/1920),round(40*self.screen_width/1920)))
            else:
                self.image = pygame.transform.scale(pygame.image.load("Images/strength_potion.png").convert_alpha(),(round(40*self.screen_height/1080),round(40*self.screen_height/1080)))
        elif(self.random_value == 2):
            self.name = "slow_alien_lasers"
            if (self.screen_width/1920 < self.screen_height/1080):
                self.image = pygame.transform.scale(pygame.image.load("Images/slow_falling_potion.png").convert_alpha(),(round(40*self.screen_width/1920),round(40*self.screen_width/1920)))
            else:
                self.image = pygame.transform.scale(pygame.image.load("Images/slow_falling_potion.png").convert_alpha(),(round(40*self.screen_height/1080),round(40*self.screen_height/1080)))
        self.speed = speed
        self.rect = self.image.get_rect(center = pos)

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.screen_height + 50:
            self.kill()

    def update(self):
        self.rect.y += round(self.speed*self.screen_height/1080)
        self.destroy()