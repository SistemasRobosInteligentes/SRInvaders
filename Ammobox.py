import pygame

class Ammobox(pygame.sprite.Sprite):
    def __init__(self,side,screen_width,camera_height,screen_height):
        super().__init__()
        self.image = pygame.image.load('Images/quiver.png').convert_alpha()
        if side == 'right':
            x = screen_width/2 + 310
        if side == 'left':
            x = screen_width/2 - 350
            
            
            
        self.rect = self.image.get_rect(topleft = (x,screen_height+150)) #

    def update(self):
        self.rect.x += 0