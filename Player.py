import pygame, sys
from random import choice, randint
from threading import Thread, Event

#SELF MADE CODE IMPORTS
import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,constraint,speed):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.number_lasers = 1
        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound('bow.wav')
        self.laser_sound.set_volume(0.2)

    def get_input(self):
        keys = pygame.key.get_pressed()

#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.speed
#         elif keys[pygame.K_LEFT]:
#             self.rect.x -= self.speed
    
    def handle_lasers(self, user):
        if self.ready and user.may_shoot:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        if(self.number_lasers == 1):
            self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))
        elif(self.number_lasers == 2):
            self.lasers.add(Laser([self.rect.center[0] - 8,self.rect.center[1]],-8,self.rect.bottom))
            self.lasers.add(Laser([self.rect.center[0] + 8,self.rect.center[1]],-8,self.rect.bottom))
        elif(self.number_lasers == 3):
            self.lasers.add(Laser([self.rect.center[0] - 12,self.rect.center[1]],-8,self.rect.bottom))
            self.lasers.add(Laser([self.rect.center[0],self.rect.center[1]],-8,self.rect.bottom))
            self.lasers.add(Laser([self.rect.center[0] + 12,self.rect.center[1]],-8,self.rect.bottom))
        else:
            self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom)) 

    def update(self, user):
        self.handle_lasers(user)
        self.get_input()
        self.rect.x = user.x_pos
        #print(user.x_pos)
        self.constraint()
        self.recharge()
        self.lasers.update()
