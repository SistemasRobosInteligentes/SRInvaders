import pygame, sys
from random import choice, randint
from threading import Thread, Event

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width,camera_height):
        super().__init__()
        self.image = pygame.image.load('Images/extra.png').convert_alpha()
        
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,60+camera_height))

    def update(self):
        self.rect.x += self.speed