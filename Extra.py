import pygame

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width,camera_height, screen_height):
        super().__init__()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.image = pygame.transform.scale(pygame.image.load('Images/extra.png').convert_alpha(),(round(50*self.screen_width/1920),round(50*self.screen_width/1920)))
        else:
            self.image = pygame.transform.scale(pygame.image.load('Images/extra.png').convert_alpha(),(round(50*self.screen_height/1080),round(50*self.screen_height/1080)))
        
        if side == 'right':
            x = screen_width + 50
            self.speed = - round(3 * screen_width/1920)
        else:
            x = -50
            self.speed = round(3 * screen_width/1920)

        self.rect = self.image.get_rect(topleft = (x, screen_height*60/1080+camera_height))

    def update(self):
        self.rect.x += self.speed