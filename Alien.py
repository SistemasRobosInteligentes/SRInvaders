import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y,file_path, screen_height, screen_width):
        super().__init__()
        
        self.screen_height = screen_height
        self.screen_width = screen_width
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.image = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(),(round(45*self.screen_width/1920),round(45*self.screen_width/1920)))
        else:
            self.image = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(),(round(45*self.screen_height/1080),round(45*self.screen_height/1080)))
        
        self.rect = self.image.get_rect(topleft = (x,y))
        
        if color == 'tier1': 
            self.value = 100
            self.life = 1
        elif color == 'tier2': 
            self.value = 200
            self.life = 2
        elif color == 'tier3': 
            self.value = 300
            self.life = 3

    def update(self,direction):
        self.rect.x += direction