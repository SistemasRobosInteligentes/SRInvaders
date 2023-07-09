import pygame

#SELF MADE CODE IMPORTS
from Laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self,pos, screen_width, screen_height, camera_height):
        super().__init__()
        
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.camera_height = camera_height
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.image = pygame.transform.scale(pygame.image.load('Images/player.png').convert_alpha(),(round(45*self.screen_width/1920),round(45*self.screen_width/1920)))
        else:
            self.image = pygame.transform.scale(pygame.image.load('Images/player.png').convert_alpha(),(round(45*self.screen_height/1080),round(45*self.screen_height/1080)))
        
        self.rect = self.image.get_rect(midbottom = pos)
        self.max_x_constraint = screen_width
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.number_lasers = 1
        self.lasers_quiver = 15                                #Testing max Ammo
        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('Sounds/bow.wav')
        self.laser_sound.set_volume(0.2)

    def get_input(self):
        keys = pygame.key.get_pressed()

    def muteSound(self):
        self.laser_sound.set_volume(0)


    
    def handle_lasers(self, user):
        if self.ready and user.may_shoot and user.pull_string==True:
          if self.lasers_quiver > 0:                            #Testing max Ammo
            self.shoot_laser()
            self.lasers_quiver = self.lasers_quiver - 1          #Ammo Going Down
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
        if user.squat==True:
            if (pygame.time.get_ticks())%30 == 0:
                self.lasers_quiver = self.lasers_quiver + 3
                #print("Fez o Squat")
                #print(self.lasers_quiver)
                user.squat = False

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
            self.lasers.add(Laser(self.rect.center,-8,self.screen_height, self.screen_width, self.camera_height))
        elif(self.number_lasers == 2):
            self.lasers.add(Laser([self.rect.center[0] - 8,self.rect.center[1]],-8,self.screen_height, self.screen_width, self.camera_height))
            self.lasers.add(Laser([self.rect.center[0] + 8,self.rect.center[1]],-8,self.screen_height, self.screen_width, self.camera_height))
        elif(self.number_lasers == 3):
            self.lasers.add(Laser([self.rect.center[0] - 12,self.rect.center[1]],-8,self.screen_height, self.screen_width, self.camera_height))
            self.lasers.add(Laser([self.rect.center[0],self.rect.center[1]],-8,self.screen_height, self.screen_width, self.camera_height))
            self.lasers.add(Laser([self.rect.center[0] + 12,self.rect.center[1]],-8,self.screen_height, self.screen_width, self.camera_height))
        else:
            self.lasers.add(Laser(self.rect.center,-8,self.screen_height, self.screen_width, self.camera_height)) 

    def update(self, user):
        self.handle_lasers(user)
        self.get_input()
        self.rect.x = user.x_pos
        self.constraint()
        self.recharge()
        self.lasers.update()
