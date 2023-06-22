import pygame, sys
from random import choice, randint
from threading import Thread, Event

class Powerups(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screen_height):
        super().__init__()
        self.random_value = randint(0,2)
        if(self.random_value == 0):
            self.name = "plus_1_life"
            self.image = pygame.image.load("Images/golden_apple.png").convert_alpha()
        elif(self.random_value == 1):
            self.name = "plus_1_arrow"
            self.image = pygame.image.load("Images/strength_potion.png")
        elif(self.random_value == 2):
            self.name = "slow_alien_lasers"
            self.image = pygame.image.load("Images/slow_falling_potion.png")
        self.speed = speed
        self.rect = self.image.get_rect(center = pos)
        self.height_y_constraint = screen_height   

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()